from enum import Enum
from abc import ABC, ABCMeta, abstractmethod
from typing import Callable, Any, Self

import yaml
from attrs import define


def register_loader(loader) -> Any: ...


def register_dumper(dumper) -> Any: ...


def register_load(tag: str, func_load: Callable[Any, Any]) -> Any: ...


def register_dump(type_dump: type, func_dump: Callable[Any, yaml.Node]) -> Any: ...


class MetaYamlSerialized(ABCMeta):
    def __init__(cls, name, bases, namespace) -> Any: ...
    
    def tag(cls) -> Any: ...


class YamlSerialized(ABC):
    @classmethod
    def dump_yaml(cls, dumper: yaml.BaseDumper, data: Self) -> Any: ...
    
    @abstractmethod
    def save(self) -> Any: ...
    
    @classmethod
    def load_yaml(cls, loader: yaml.BaseLoader, node: yaml.MappingNode) -> Any: ...
    
    @classmethod
    @abstractmethod
    def restore(cls, data: dict) -> Any: ...


def yaml_enum_serialized(cls_enum: type[Enum]) -> Any: ...


@define
class Storage:
    dumper: yaml.BaseDumper
    loader: yaml.BaseLoader
    
    def load(self, stream) -> Any: ...
    
    def dump(self, data, stream) -> Any: ...
