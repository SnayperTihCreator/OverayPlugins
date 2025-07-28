from typing import Any

from .config import Config

def save(path, config: Config, data: dict): ...

def load(path, config: Config)->Any: ...