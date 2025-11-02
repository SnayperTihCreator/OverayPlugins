from enum import Enum

import yaml

from .core import register_load, register_dump


def yaml_enum_serialized(cls_enum: type[Enum]):
    if not hasattr(cls_enum, "save"):
        raise TypeError("not found classmethod <save>")
    
    def dump_yaml(dumper: yaml.BaseDumper, data: Enum):
        return dumper.represent_scalar(f"!{cls_enum.__module__}.{cls_enum.__name__}", data.save())
    
    register_dump(cls_enum, dump_yaml)
    
    if not hasattr(cls_enum, "restore"):
        raise TypeError("not found classmethod <restore>")
    
    def load_yaml(loader: yaml.BaseLoader, node: yaml.ScalarNode):
        data = loader.construct_scalar(node)
        return cls_enum.restore(data)
    
    register_load(f"!{cls_enum.__module__}.{cls_enum.__name__}", load_yaml)
    
    return cls_enum
