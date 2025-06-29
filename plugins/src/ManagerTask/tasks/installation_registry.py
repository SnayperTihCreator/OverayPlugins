from datetime import datetime, timedelta

import yaml

from .core import registry_to_yaml, registry_from_yaml


def rep_datetime(dumper: yaml.Dumper, data: datetime):
    return dumper.represent_scalar("!datetime", data.isoformat())


def con_datetime(loader: yaml.Loader, node):
    return datetime.fromisoformat(loader.construct_scalar(node))


registry_to_yaml(datetime, rep_datetime)
registry_from_yaml("!datetime", con_datetime)


def rep_dt(dumper: yaml.Dumper, data: timedelta):
    return dumper.represent_scalar("!timedelta", str(data.seconds))


def con_dt(loader: yaml.Loader, node):
    return timedelta(seconds=int(loader.construct_scalar(node)))


registry_to_yaml(timedelta, rep_dt)
registry_from_yaml("!timedelta", con_dt)