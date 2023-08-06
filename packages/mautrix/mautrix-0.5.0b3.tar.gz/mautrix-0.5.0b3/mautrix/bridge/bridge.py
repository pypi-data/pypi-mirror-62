# Copyright (c) 2020 Tulir Asokan
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import Iterable, Awaitable, Optional, Type
from time import time
import argparse
import logging
import logging.config
import asyncio
import signal
import copy
import sys

import sqlalchemy as sql
from sqlalchemy.engine.base import Engine

from mautrix.appservice import AppService
from ..util.db import Base
from .db import SQLStateStore
from .config import BaseBridgeConfig, ConfigValueError
from .matrix import BaseMatrixHandler

try:
    import uvloop
except ImportError:
    uvloop = None


class Bridge:
    loop: asyncio.AbstractEventLoop
    log: logging.Logger
    parser: argparse.ArgumentParser
    db: Engine
    az: AppService
    state_store_class: Type[SQLStateStore] = SQLStateStore
    state_store: SQLStateStore
    config_class: Type[BaseBridgeConfig]
    config: BaseBridgeConfig
    matrix_class: Type[BaseMatrixHandler]
    matrix: BaseMatrixHandler
    startup_actions: Optional[Iterable[Awaitable]]
    shutdown_actions: Optional[Iterable[Awaitable]]
    name: str
    args: argparse.Namespace
    version: str
    repo_url: str
    markdown_version: str
    command: str
    description: str
    real_user_content_key: Optional[str] = None

    def __init__(self, name: str = None, description: str = None, command: str = None,
                 version: str = None, real_user_content_key: Optional[str] = None,
                 config_class: Type[BaseBridgeConfig] = None,
                 matrix_class: Type[BaseMatrixHandler] = None,
                 state_store_class: Type[SQLStateStore] = None) -> None:
        if name:
            self.name = name
        if description:
            self.description = description
        if command:
            self.command = command
        if real_user_content_key:
            self.real_user_content_key = real_user_content_key
        if version:
            self.version = version
        if config_class:
            self.config_class = config_class
        if matrix_class:
            self.matrix_class = matrix_class
        if state_store_class:
            self.state_store_class = state_store_class
        self.startup_actions = None
        self.shutdown_actions = None

    def run(self) -> None:
        """
        Prepare and run the bridge. This is the main entrypoint and the only function that should
        be called manually.
        """
        self._prepare()
        self._run()

    def prepare_arg_parser(self) -> None:
        self.parser = argparse.ArgumentParser(description=self.description, prog=self.command)
        self.parser.add_argument("-c", "--config", type=str, default="config.yaml",
                                 metavar="<path>", help="the path to your config file")
        self.parser.add_argument("-b", "--base-config", type=str, default="example-config.yaml",
                                 metavar="<path>", help="the path to the example config "
                                                        "(for automatic config updates)")
        self.parser.add_argument("-g", "--generate-registration", action="store_true",
                                 help="generate registration and quit")
        self.parser.add_argument("-r", "--registration", type=str, default="registration.yaml",
                                 metavar="<path>",
                                 help="the path to save the generated registration to (not needed "
                                      "for running the bridge)")

    def _prepare(self) -> None:
        start_ts = time()
        self.prepare_arg_parser()
        self.args = self.parser.parse_args()

        self.prepare_config(self.args.config, self.args.registration, self.args.base_config)
        self.prepare_log()
        self.check_config(check_tokens=not self.args.generate_registration)

        if self.args.generate_registration:
            self.generate_registration()
            sys.exit(0)

        self.log.debug(f"Initializing {self.name} {self.version}")
        try:
            self.prepare_loop()
            self.prepare_appservice()
            self.prepare_db()
            self.prepare_bridge()
        except Exception:
            self.log.critical("Unexpected error in initialization", exc_info=True)
            sys.exit(1)
        end_ts = time()
        self.log.debug(f"Initialization complete in {round(end_ts - start_ts, 2)} seconds")

    def prepare_config(self, config: str, registration: str, base_config: str) -> None:
        self.config = self.config_class(config, registration, base_config)
        self.config.load()
        self.config.update()

    def check_config(self, check_tokens: bool = True) -> None:
        try:
            self.config._check_tokens = check_tokens
            self.config.check_default_values()
        except ConfigValueError as e:
            self.log.fatal(f"Configuration error: {e}")
            sys.exit(11)

    def generate_registration(self) -> None:
        self.config.generate_registration()
        self.config.save()
        print(f"Registration generated and saved to {self.config.registration_path}")

    def prepare_log(self) -> None:
        logging.config.dictConfig(copy.deepcopy(self.config["logging"]))
        self.log = logging.getLogger("mau.init")

    def prepare_loop(self) -> None:
        if uvloop:
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
            self.log.debug("Using uvloop for asyncio")

        self.loop = asyncio.get_event_loop()

    def prepare_appservice(self) -> None:
        self.state_store = self.state_store_class()
        mb = 1024 ** 2
        self.az = AppService(server=self.config["homeserver.address"],
                             domain=self.config["homeserver.domain"],
                             verify_ssl=self.config["homeserver.verify_ssl"],

                             as_token=self.config["appservice.as_token"],
                             hs_token=self.config["appservice.hs_token"],

                             bot_localpart=self.config["appservice.bot_username"],

                             log="mau.as",
                             loop=self.loop,

                             state_store=self.state_store,

                             real_user_content_key=self.real_user_content_key,

                             aiohttp_params={
                                 "client_max_size": self.config["appservice.max_body_size"] * mb
                             })

        signal.signal(signal.SIGINT, signal.default_int_handler)
        signal.signal(signal.SIGTERM, signal.default_int_handler)

    def prepare_db(self) -> None:
        self.db = sql.create_engine(self.config["appservice.database"])
        Base.metadata.bind = self.db
        if not self.db.has_table("alembic_version"):
            self.log.critical("alembic_version table not found. "
                              "Did you forget to `alembic upgrade head`?")
            sys.exit(10)

    def prepare_bridge(self) -> None:
        self.matrix = self.matrix_class(az=self.az, config=self.config, loop=self.loop, bridge=self)

    def _run(self) -> None:
        try:
            self.log.debug("Running startup actions...")
            start_ts = time()
            self.loop.run_until_complete(self.start())
            end_ts = time()
            self.log.debug(f"Startup actions complete in {round(end_ts - start_ts, 2)} seconds, "
                           "now running forever")
            self.az.ready = True
            self._stop_task = self.loop.create_future()
            self.loop.run_until_complete(self._stop_task)
            self.log.debug("manual_stop() called, stopping...")
        except KeyboardInterrupt:
            self.log.debug("Interrupt received, stopping...")
        except Exception:
            self.log.critical("Unexpected error in main event loop", exc_info=True)
            sys.exit(2)
        self.prepare_stop()
        self.loop.run_until_complete(self.stop())
        self.prepare_shutdown()
        self.log.info("Everything stopped, shutting down")
        sys.exit(0)

    async def start(self) -> None:
        self.log.debug("Starting appservice...")
        await self.az.start(self.config["appservice.hostname"], self.config["appservice.port"])
        await self.matrix.wait_for_connection()
        await self._run_startup_actions()

    async def _run_startup_actions(self) -> None:
        await asyncio.gather(self.matrix.init_as_bot(), *(self.startup_actions or []),
                             loop=self.loop)

    def prepare_stop(self) -> None:
        """
        Lifecycle method that is called before awaiting :meth:`stop`.
        Useful to fill shutdown_actions.
        """
        pass

    async def stop(self) -> None:
        await self.az.stop()
        await asyncio.gather(*(self.shutdown_actions or []), loop=self.loop)

    def prepare_shutdown(self) -> None:
        """Lifecycle method that is called right before ``sys.exit(0)``."""
        pass

    def manual_stop(self) -> None:
        self._stop_task.set_result(None)
