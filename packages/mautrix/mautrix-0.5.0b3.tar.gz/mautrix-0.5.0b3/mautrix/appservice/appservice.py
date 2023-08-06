# Copyright (c) 2020 Tulir Asokan
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Partly based on github.com/Cadair/python-appservice-framework (MIT license)
from typing import Optional, Callable, Awaitable, Union, List, Dict
from aiohttp import web
import aiohttp
import asyncio
import logging

from ..api import JSON
from ..types import UserID, RoomAlias, Event, SerializerError
from .api import AppServiceAPI, IntentAPI
from .state_store import StateStore, JSONStateStore

QueryFunc = Callable[[web.Request], Awaitable[Optional[web.Response]]]
HandlerFunc = Callable[[Event], Awaitable]


class AppService:
    """The main AppService container."""

    server: str
    domain: str
    verify_ssl: bool
    as_token: str
    hs_token: str
    bot_mxid: UserID
    real_user_content_key: str
    state_store: StateStore

    transactions: List[str]

    query_user: Callable[[UserID], JSON]
    query_alias: Callable[[RoomAlias], JSON]
    ready: bool
    live: bool

    loop: asyncio.AbstractEventLoop
    log: logging.Logger
    app: web.Application

    def __init__(self, server: str, domain: str, as_token: str, hs_token: str, bot_localpart: str,
                 loop: Optional[asyncio.AbstractEventLoop] = None,
                 log: Optional[Union[logging.Logger, str]] = None, verify_ssl: bool = True,
                 query_user: QueryFunc = None, query_alias: QueryFunc = None,
                 real_user_content_key: Optional[str] = "net.maunium.appservice.puppet",
                 state_store: StateStore = None, aiohttp_params: Dict = None) -> None:
        self.server = server
        self.domain = domain
        self.verify_ssl = verify_ssl
        self.as_token = as_token
        self.hs_token = hs_token
        self.bot_mxid = UserID(f"@{bot_localpart}:{domain}")
        self.real_user_content_key: str = real_user_content_key
        if isinstance(state_store, StateStore):
            self.state_store = state_store
        else:
            file = state_store if isinstance(state_store, str) else "mx-state.json"
            self.state_store: JSONStateStore = JSONStateStore(autosave_file=file)
            self.state_store.load(file)

        self.transactions = []

        self._http_session = None
        self._intent = None

        self.loop = loop or asyncio.get_event_loop()
        self.log = (logging.getLogger(log) if isinstance(log, str)
                    else log or logging.getLogger("mautrix_appservice"))

        async def default_query_handler(_):
            return None

        self.query_user = query_user or default_query_handler
        self.query_alias = query_alias or default_query_handler
        self.live = True
        self.ready = False

        self.event_handlers = []

        self.app = web.Application(loop=self.loop, **aiohttp_params if aiohttp_params else {})
        self.app.router.add_route("PUT", "/transactions/{transaction_id}",
                                  self._http_handle_transaction)
        self.app.router.add_route("GET", "/rooms/{alias}", self._http_query_alias)
        self.app.router.add_route("GET", "/users/{user_id}", self._http_query_user)
        self.app.router.add_route("PUT", "/_matrix/app/v1/transactions/{transaction_id}",
                                  self._http_handle_transaction)
        self.app.router.add_route("GET", "/_matrix/app/v1/rooms/{alias}", self._http_query_alias)
        self.app.router.add_route("GET", "/_matrix/app/v1/users/{user_id}", self._http_query_user)
        self.app.router.add_route("GET", "/_matrix/mau/live", self._liveness_probe)
        self.app.router.add_route("GET", "/_matrix/mau/ready", self._readiness_probe)

        async def update_state(event: Event):
            self.state_store.update_state(event)

        self.matrix_event_handler(update_state)

    @property
    def http_session(self) -> aiohttp.ClientSession:
        if self._http_session is None:
            raise AttributeError("the http_session attribute can only be used after starting")
        else:
            return self._http_session

    @property
    def intent(self) -> 'IntentAPI':
        if self._intent is None:
            raise AttributeError("the intent attribute can only be used after starting")
        else:
            return self._intent

    async def __aenter__(self) -> None:
        await self.start()

    async def __aexit__(self) -> None:
        await self.stop()

    async def start(self, host: str = "127.0.0.1", port: int = 8080) -> None:
        connector = None
        self.log.debug(f"Starting appservice web server on {host}:{port}")
        if self.server.startswith("https://") and not self.verify_ssl:
            connector = aiohttp.TCPConnector(verify_ssl=False)
        self._http_session = aiohttp.ClientSession(loop=self.loop, connector=connector)
        self._intent = AppServiceAPI(base_url=self.server, bot_mxid=self.bot_mxid, log=self.log,
                                     token=self.as_token, state_store=self.state_store,
                                     real_user_content_key=self.real_user_content_key,
                                     client_session=self._http_session).bot_intent()

        await self.loop.create_server(self.app.make_handler(), host, port)

    async def stop(self) -> None:
        self.log.debug("Stopping appservice web server")
        self._intent = None
        await self._http_session.close()
        self._http_session = None

    def _check_token(self, request: web.Request) -> bool:
        try:
            token = request.rel_url.query["access_token"]
        except KeyError:
            return False

        if token != self.hs_token:
            return False

        return True

    async def _liveness_probe(self, _: web.Request) -> web.Response:
        return web.Response(status=200 if self.live else 500, text="{}")

    async def _readiness_probe(self, _: web.Request) -> web.Response:
        return web.Response(status=200 if self.ready else 500, text="{}")

    async def _http_query_user(self, request: web.Request) -> web.Response:
        if not self._check_token(request):
            return web.Response(status=401)

        try:
            user_id = request.match_info["userId"]
        except KeyError:
            return web.Response(status=400)

        try:
            response = await self.query_user(user_id)
        except Exception:
            self.log.exception("Exception in user query handler")
            return web.Response(status=500)

        if not response:
            return web.Response(status=404)
        return web.json_response(response)

    async def _http_query_alias(self, request: web.Request) -> web.Response:
        if not self._check_token(request):
            return web.Response(status=401)

        try:
            alias = request.match_info["alias"]
        except KeyError:
            return web.Response(status=400)

        try:
            response = await self.query_alias(alias)
        except Exception:
            self.log.exception("Exception in alias query handler")
            return web.Response(status=500)

        if not response:
            return web.Response(status=404)
        return web.json_response(response)

    async def _http_handle_transaction(self, request: web.Request) -> web.Response:
        if not self._check_token(request):
            return web.Response(status=401)

        transaction_id = request.match_info["transaction_id"]
        if transaction_id in self.transactions:
            return web.json_response({})  # 200 OK

        json = await request.json()

        try:
            events = json["events"]
        except KeyError:
            return web.Response(status=400)

        for raw_event in events:
            try:
                event = Event.deserialize(raw_event)
            except SerializerError:
                self.log.exception("Failed to deserialize event %s", raw_event)
            else:
                self.handle_matrix_event(event)

        self.transactions.append(transaction_id)

        return web.json_response({})

    def handle_matrix_event(self, event: Event) -> None:
        if event.type.is_state and event.state_key is None:
            self.log.debug(f"Not sending {event.event_id} to handlers: expected state_key.")
            return

        async def try_handle(handler_func: HandlerFunc):
            try:
                await handler_func(event)
            except Exception:
                self.log.exception("Exception in Matrix event handler")

        for handler in self.event_handlers:
            asyncio.ensure_future(try_handle(handler), loop=self.loop)

    def matrix_event_handler(self, func: HandlerFunc) -> HandlerFunc:
        self.event_handlers.append(func)
        return func
