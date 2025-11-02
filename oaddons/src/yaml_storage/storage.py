from attrs import define, field
import yaml


@define
class Storage:
    dumper: yaml.BaseDumper = field(default=yaml.SafeDumper)
    loader: yaml.BaseLoader = field(default=yaml.SafeLoader)
    
    def load(self, stream):
        if isinstance(stream, str):
            with open(stream, encoding="utf-8") as file:
                return self.load(file)
        return yaml.load(stream, self.loader)
    
    def dump(self, data, stream):
        if isinstance(stream, str):
            with open(stream, "w", encoding="utf-8") as file:
                self.dump(data, file)
        yaml.dump(data, stream, self.dumper)
