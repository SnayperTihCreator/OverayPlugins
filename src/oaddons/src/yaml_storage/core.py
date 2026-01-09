from abc import ABC, ABCMeta, abstractmethod
import yaml
from typing import Callable, Any, Self

_loaders = [yaml.Loader, yaml.SafeLoader, yaml.FullLoader, yaml.UnsafeLoader]
_dumpers = [yaml.Dumper, yaml.SafeDumper]


def register_loader(loader):
    _loaders.append(loader)
    return loader


def register_dumper(dumper):
    _dumpers.append(dumper)


def register_load(tag: str, func_load: Callable[[yaml.BaseLoader, Any], Any]):
    for loader in _loaders:
        loader.add_constructor(tag, func_load)


def register_dump(type_dump: type, func_dump: Callable[[yaml.BaseDumper, Any], yaml.Node]):
    for dumper in _dumpers:
        dumper.add_representer(type_dump, func_dump)


class MetaYamlSerialized(ABCMeta):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        register_dump(cls, cls.dump_yaml)
        register_load(cls.tag(), cls.load_yaml)
    
    def tag(cls):
        return f"!{cls.__module__}.{cls.__name__}"


class YamlSerialized(ABC, metaclass=MetaYamlSerialized):
    
    @classmethod
    def dump_yaml(cls, dumper: yaml.BaseDumper, data: Self):
        return dumper.represent_mapping(
            cls.tag(),
            data.save()
        )
    
    @abstractmethod
    def save(self):
        return {}
    
    @classmethod
    def load_yaml(cls, loader: yaml.BaseLoader, node: yaml.MappingNode):
        data = loader.construct_mapping(node, True)
        return cls.restore(data)
    
    @classmethod
    @abstractmethod
    def restore(cls, data: dict):
        return cls()


try:
    from PySide6.QtCore import QObject
    
    QMetaObject = type(QObject)
    
    
    class QMetaYamlSerialized(MetaYamlSerialized, QMetaObject):
        def __init__(cls, name, bases, namespace):
            super(QMetaObject, cls).__init__(name, bases, namespace)
            super().__init__(name, bases, namespace)
    
    
    class QYamlSerialized(QObject, YamlSerialized, ABC, metaclass=QMetaYamlSerialized):
        def __init__(self, parent=None):
            super().__init__(parent)

except ImportError:
    QMetaYamlSerialized = None
    QYamlSerialized = None
