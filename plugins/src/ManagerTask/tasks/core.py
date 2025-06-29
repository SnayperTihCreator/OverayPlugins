from abc import ABCMeta, abstractmethod
from typing import Self

import yaml
from PySide6.QtCore import QObject


def registry_to_yaml(data_type, to_yaml):
    yaml.SafeDumper.add_representer(data_type, to_yaml)


def registry_from_yaml(tag, from_yaml):
    yaml.SafeLoader.add_constructor(tag, from_yaml)


class MetaABCObject(ABCMeta, type(QObject)):
    
    def __init__(cls, name, bases, namespace):
        type(QObject).__init__(cls, name, bases, namespace)
        ABCMeta.__init__(cls, name, bases, namespace)
        
        registry_to_yaml(cls, cls.to_yaml)
        registry_from_yaml(f"!{cls.__module__}.{name}", cls.from_yaml)


class QABCObject(QObject, metaclass=MetaABCObject):
    yaml_flow_style = None
    
    yaml_loader = yaml.SafeLoader
    yaml_dumper = yaml.SafeDumper
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
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
