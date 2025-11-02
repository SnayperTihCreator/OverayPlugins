from datetime import datetime, timedelta

import yaml

from OExtension.yaml_storage import register_load, register_dump


def rep_datetime(dumper: yaml.Dumper, data: datetime):
    return dumper.represent_scalar("!datetime", data.isoformat())


def con_datetime(loader: yaml.Loader, node):
    return datetime.fromisoformat(loader.construct_scalar(node))


register_dump(datetime, rep_datetime)
register_load("!datetime", con_datetime)


def rep_dt(dumper: yaml.Dumper, data: timedelta):
    return dumper.represent_scalar("!timedelta", str(data.seconds))


def con_dt(loader: yaml.Loader, node):
    return timedelta(seconds=int(loader.construct_scalar(node)))


register_dump(timedelta, rep_dt)
register_load("!timedelta", con_dt)
