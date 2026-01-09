import textwrap
import pathlib
from xml.etree.ElementTree import parse
import sys

import jinja2


def toCamelCase(data: str):
    return data[0].lower() + data[1:]


class XMLSchemaLoader(jinja2.BaseLoader):
    def __init__(self, path):
        self.root = parse(path).getroot()
        self.templates = {temp.get("name"): temp for temp in self.root}
    
    def get_source(self, environment: jinja2.Environment, template: str):
        temp_element = self.templates.get(template)
        content = temp_element.find("content")
        return textwrap.dedent(content.text).strip(), template, lambda: True


def buildEnv(path) -> jinja2.Environment:
    loader = XMLSchemaLoader(path)
    env = jinja2.Environment(loader=loader)
    env.filters["camelCase"] = toCamelCase
    return env


def buildFileContent(path: pathlib.Path, content: str, exist_ok=True):
    path.touch(exist_ok=exist_ok)
    return path.write_text(content, "utf-8")


def getAppPath():
    if getattr(sys, 'frozen', False):
        return pathlib.Path(sys._MEIPASS)
    else:
        return pathlib.Path(__file__).parent.parent
