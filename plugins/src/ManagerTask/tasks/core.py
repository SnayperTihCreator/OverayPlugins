from abc import ABCMeta, abstractmethod
from typing import Self

import yaml


def registry_to_yaml(dumper: type[yaml.Dumper], data_type, to_yaml):
    dumper.add_representer(data_type, to_yaml)


def registry_from_yaml(loaders: list[type[yaml.Loader]] | type[yaml.Loader], tag, from_yaml):
    if isinstance(loaders, list):
        for loader in loaders:
            loader.add_constructor(tag, from_yaml)
    else:
        loaders.add_constructor(tag, from_yaml)


class MetaABCObject(ABCMeta):
    yaml_dumper: type[yaml.Dumper]
    yaml_loader: list[type[yaml.Loader]] | type[yaml.Loader]
    
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        registry_to_yaml(cls.yaml_dumper, cls, cls.to_yaml)
        registry_from_yaml(cls.yaml_loader, f"!{cls.__module__}.{name}", cls.from_yaml)


class ABCObject(metaclass=MetaABCObject):
    yaml_flow_style = None
    
    yaml_loader = yaml.SafeLoader
    yaml_dumper = yaml.SafeDumper
    
    @classmethod
    def from_yaml(cls, loader: yaml.Loader, node):
        data = loader.construct_mapping(node, True)
        return cls.restore(data)
    
    @classmethod
    def to_yaml(cls, dumper: yaml.Dumper, data: Self):
        return dumper.represent_mapping(
            f"!{cls.__module__}.{cls.__name__}",
            data.save()
        )
    
    @classmethod
    @abstractmethod
    def restore(cls, data):
        return cls()
    
    @abstractmethod
    def save(self):
        return {}
