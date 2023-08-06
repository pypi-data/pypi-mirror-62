# Copyright (c) 2020 Tulir Asokan
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import Any, Optional, Tuple, Callable, Generic, TypeVar, Type
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from abc import ABC, abstractmethod
import logging
import copy
import io

yaml = YAML()
yaml.indent(4)
yaml.width = 200

T = TypeVar('T')

log: logging.Logger = logging.getLogger("mau.util.config")


class RecursiveDict(Generic[T]):
    def __init__(self, data: Optional[T] = None, dict_factory: Optional[Type[T]] = None) -> None:
        self._dict_factory = dict_factory or dict
        self._data: CommentedMap = data or self._dict_factory()

    def clone(self) -> 'RecursiveDict':
        return RecursiveDict(data=copy.deepcopy(self._data), dict_factory=self._dict_factory)

    @staticmethod
    def parse_key(key: str) -> Tuple[str, Optional[str]]:
        if '.' not in key:
            return key, None
        key, next_key = key.split('.', 1)
        if len(key) > 0 and key[0] == "[":
            end_index = next_key.index("]")
            key = key[1:] + "." + next_key[:end_index]
            next_key = next_key[end_index + 2:] if len(next_key) > end_index + 1 else None
        return key, next_key

    def _recursive_get(self, data: T, key: str, default_value: Any) -> Any:
        key, next_key = self.parse_key(key)
        if next_key is not None:
            next_data = data.get(key, self._dict_factory())
            return self._recursive_get(next_data, next_key, default_value)
        try:
            return data[key]
        except (AttributeError, KeyError):
            return default_value

    def get(self, key: str, default_value: Any, allow_recursion: bool = True) -> Any:
        if allow_recursion and '.' in key:
            return self._recursive_get(self._data, key, default_value)
        return self._data.get(key, default_value)

    def __getitem__(self, key: str) -> Any:
        return self.get(key, None)

    def __contains__(self, key: str) -> bool:
        return self.get(key, None) is not None

    def _recursive_set(self, data: T, key: str, value: Any) -> None:
        key, next_key = self.parse_key(key)
        if next_key is not None:
            if key not in data:
                data[key] = self._dict_factory()
            next_data = data.get(key, self._dict_factory())
            return self._recursive_set(next_data, next_key, value)
        data[key] = value

    def set(self, key: str, value: Any, allow_recursion: bool = True) -> None:
        if allow_recursion and '.' in key:
            self._recursive_set(self._data, key, value)
            return
        self._data[key] = value

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)

    def _recursive_del(self, data: T, key: str) -> None:
        key, next_key = self.parse_key(key)
        if next_key is not None:
            if key not in data:
                return
            next_data = data[key]
            return self._recursive_del(next_data, next_key)
        try:
            del data[key]
            del data.ca.items[key]
        except KeyError:
            pass

    def delete(self, key: str, allow_recursion: bool = True) -> None:
        if allow_recursion and '.' in key:
            self._recursive_del(self._data, key)
            return
        try:
            del self._data[key]
            del self._data.ca.items[key]
        except KeyError:
            pass

    def __delitem__(self, key: str) -> None:
        self.delete(key)


class ConfigUpdateHelper:
    base: RecursiveDict[CommentedMap]

    def __init__(self, base: RecursiveDict, config: RecursiveDict) -> None:
        self.base = base
        self.source = config

    def copy(self, from_path: str, to_path: Optional[str] = None) -> None:
        if from_path in self.source:
            self.base[to_path or from_path] = self.source[from_path]

    def copy_dict(self, from_path: str, to_path: Optional[str] = None,
                  override_existing_map: Optional[bool] = True) -> None:
        if from_path in self.source:
            to_path = to_path or from_path
            if override_existing_map or to_path not in self.base:
                self.base[to_path] = CommentedMap()
            for key, value in self.source[from_path].items():
                self.base[to_path][key] = value

    def __iter__(self):
        yield self.copy
        yield self.copy_dict
        yield self.base


class BaseConfig(ABC, RecursiveDict[CommentedMap]):
    @abstractmethod
    def load(self) -> None:
        pass

    @abstractmethod
    def load_base(self) -> Optional[RecursiveDict[CommentedMap]]:
        pass

    def load_and_update(self) -> None:
        self.load()
        self.update()

    @abstractmethod
    def save(self) -> None:
        pass

    def update(self) -> None:
        base = self.load_base()
        if not base:
            raise ValueError("Can't update() without base config")

        self.do_update(ConfigUpdateHelper(base, self))
        self._data = base._data
        self.save()

    @abstractmethod
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        pass


class BaseStringConfig(BaseConfig, ABC):
    def __init__(self, data: str, base_data: str) -> None:
        super().__init__()
        self._data = yaml.load(data)
        self._base = RecursiveDict(yaml.load(base_data), CommentedMap)

    def load(self) -> None:
        pass

    def load_base(self) -> Optional[RecursiveDict[CommentedMap]]:
        return self._base

    def save(self) -> str:
        buf = io.StringIO()
        yaml.dump(self._data, buf)
        return buf.getvalue()


class BaseProxyConfig(BaseConfig, ABC):
    def __init__(self, load: Callable[[], CommentedMap],
                 load_base: Callable[[], Optional[RecursiveDict[CommentedMap]]],
                 save: Callable[[RecursiveDict[CommentedMap]], None]) -> None:
        super().__init__()
        self._data = CommentedMap()
        self._load_proxy = load
        self._load_base_proxy = load_base
        self._save_proxy = save

    def load(self) -> None:
        self._data = self._load_proxy() or CommentedMap()

    def load_base(self) -> Optional[RecursiveDict[CommentedMap]]:
        return self._load_base_proxy()

    def save(self) -> None:
        self._save_proxy(self._data)


class BaseFileConfig(BaseConfig, ABC):
    def __init__(self, path: str, base_path: str) -> None:
        super().__init__()
        self._data = CommentedMap()
        self.path: str = path
        self.base_path: str = base_path

    def load(self) -> None:
        with open(self.path, 'r') as stream:
            self._data = yaml.load(stream)

    def load_base(self) -> Optional[RecursiveDict[CommentedMap]]:
        try:
            with open(self.base_path, 'r') as stream:
                return RecursiveDict(yaml.load(stream), CommentedMap)
        except OSError:
            pass
        return None

    def save(self) -> None:
        try:
            with open(self.path, 'w') as stream:
                yaml.dump(self._data, stream)
        except OSError:
            log.exception(f"Failed to overwrite the config in {self.path}")
