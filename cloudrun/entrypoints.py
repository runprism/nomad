"""
Classes for the various kinds of entrypoints users can specify within their
configuration file.
"""

# Imports
from pathlib import Path
import re
from typing import Any, Dict

# Internal imports
from cloudrun.constants import (
    SUPPORTED_ENTRYPOINTS,
)
from cloudrun.utils import (
    ConfigurationKey,
    _check_key_in_conf,
    _check_optional_key_in_conf,
)


# Metaclass
class MetaEntrypoint(type):

    classes: Dict[Any, Any] = {}

    def __new__(cls, name, bases, dct):
        result = super().__new__(cls, name, bases, dct)
        cls.classes[name.lower()] = result
        return result

    @classmethod
    def get_entrypoint(cls, name):
        return cls.classes.get(name)


# Base class
class BaseEntrypoint(metaclass=MetaEntrypoint):

    def __init__(self,
        entrypoint_conf: Dict[str, Any],
        cloudrun_wkdir: Path
    ):
        self.entrypoint_conf = entrypoint_conf
        self.cloudrun_wkdir = cloudrun_wkdir

        # Check configuration
        self.check_conf()

    def check_conf(self):
        """
        Confirm that the entrypoint configuration is acceptable
        """
        required_keys = [
            ConfigurationKey("type", str, SUPPORTED_ENTRYPOINTS),
            ConfigurationKey("cmd", str),
        ]
        for _k in required_keys:
            _check_key_in_conf(_k, self.entrypoint_conf, "entrypoint")

        # Update class attributes
        self.type = self.entrypoint_conf["type"]
        self.cmd = self.entrypoint_conf["cmd"]

    def build_command(self):
        return self.cmd


class Script(BaseEntrypoint):
    """
    Script entrypoint. We need this so out MetaEntrypoint class can create the
    appropriate child class based on the user's `type`.
    """
    pass


class Project(BaseEntrypoint):

    def check_conf(self):
        """
        Confirm that the entrypoint configuration is acceptable
        """
        super().check_conf()
        src_key = ConfigurationKey("src", str)
        _check_key_in_conf(src_key, self.entrypoint_conf, "entrypoint")

        # Update class attributes
        self.src = self.entrypoint_conf["src"]

    def build_command(self):
        return f"cd {self.src} && {self.cmd}"


class Function(BaseEntrypoint):

    def check_conf(self):
        """
        Confirm that the entrypoint configuration is acceptable
        """
        super().check_conf()
        kwargs_key = ConfigurationKey("kwargs", dict)
        _check_optional_key_in_conf(kwargs_key, self.entrypoint_conf)

        # Check the format of the `cmd`. It should be something like <module
        # name>.<function name>`.
        cmd_structure = r'(?i)^([^\.]+)\.([^\.]+)$'
        matches = re.findall(cmd_structure, self.cmd)
        if len(matches) != 1:
            raise ValueError(f"`cmd` value not properly formatted for entrypoint of type `{self.type}`")  # noqa: E501
        match = matches[0]
        self.module, self.function = match[0], match[1]

        # Update class attributes
        self.kwargs = {}
        if "kwargs" in self.entrypoint_conf.keys():
            self.kwargs = self.entrypoint_conf["kwargs"]

    def build_command(self):
        kwargs_str = ", ".join([
            f'{k}="{v}"' if isinstance(v, str) else f"{k}={v}" for k, v in self.kwargs.items()  # noqa: E501
        ])
        return f"python -c 'from {self.module} import {self.function}; {self.function}({kwargs_str})'"  # noqa: E501
