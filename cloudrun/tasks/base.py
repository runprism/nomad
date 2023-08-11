"""
Base task class
"""

# Imports
import argparse
from pathlib import Path
from typing import Any, Dict

# Internal imports
from cloudrun.constants import (
    SUPPORTED_AGENTS,
    SUPPORTED_ENTRYPOINTS,
)
from cloudrun.utils import (
    ConfigurationKey,
    _check_key_in_conf,
    _check_optional_key_in_conf,
)
from cloudrun.parsers.yml import YmlParser
from cloudrun.cloudrun_logger import (
    set_up_logger
)


# Class definition
class BaseTask:

    def __init__(self,
        args: argparse.Namespace,
    ):
        self.args = args

        # Current working directory
        self.cloudrun_wkdir = Path(self.args.wkdir)

        # Args will definitely have a `file` attribute
        self.conf_fpath = Path(self.args.file)
        raw_conf = self.parse_conf_fpath(self.conf_fpath)

        # If the user specified a specific agent to use in their args, then use that
        if hasattr(self.args, "name") and self.args.name is not None:
            self.name = args.name

        # Otherwise, the user should only have one agent in their configuration
        else:
            all_names = list(raw_conf.keys())
            if len(all_names) > 1:
                msg1 = f"multiple agents found in `{self.conf_fpath}`"
                msg2 = "specify one to use and try again"
                raise ValueError("...".join([msg1, msg2]))
            self.name = all_names[0]

        # Get the specific agent configuration
        self.conf = raw_conf[self.name]

        # Set up logger
        set_up_logger(self.args.log_level)

    def check(self):
        """
        Check all configuration requirements
        """
        self.check_conf(self.conf, self.name)
        self.confirm_matrix_conf_structure(self.conf)
        self.confirm_entrypoint_conf_structure(self.conf)
        self.confirm_additional_paths_conf_structure(self.conf)

    def parse_conf_fpath(self,
        conf_fpath: Path
    ) -> Dict[str, Any]:
        """
        Parse the configuration file path and return the configuration YAML as a
        dictionary

        args:
            conf_fpath: file path to configuration YML
        """
        parser = YmlParser(fpath=conf_fpath)
        return parser.parse()

    def check_conf(self,
        conf: Dict[str, Any],
        name: str,
    ):
        """
        Check configuration structure

        args:
            conf: agent configuration
            name: name of agent
        returns:
            True if the `conf` is properly structured
        raises:
            ValueError if `conf` is not properly structured
        """
        required_keys = [
            ConfigurationKey("type", str, SUPPORTED_AGENTS),
            ConfigurationKey("requirements", str),
            ConfigurationKey("entrypoint", dict),
            ConfigurationKey("env", dict),
        ]
        for _k in required_keys:
            _check_key_in_conf(_k, conf, name)
        return True

    def confirm_matrix_conf_structure(self,
        conf: Dict[str, Any]
    ):
        """
        Confirm that the `matrix` section of the configuration is properly structured

        args:
            conf: agent configuration
        returns:
            True if the `matrix` section is properly structured
        raises:
            ValueError() if the `matrix` section is not properly structured
        """
        if "matrix" not in conf.keys():
            return True
        matrix = conf["matrix"]

        # Only one required value: max_concurrency. This controls how many cloud
        # instances are instantiated at once
        required_keys = [
            ConfigurationKey("max_concurrency", int)
        ]
        for _k in required_keys:
            _check_key_in_conf(_k, matrix, "matrix")

        # All other values should be a list
        for key, value in matrix.items():
            if key in [_k.key_name for _k in required_keys]:
                continue
            if not isinstance(value, list):
                raise ValueError(
                    f"Invalid argument `{value}` in `matrix`...this only supports list arguments"  # noqa: E501
                )

    def confirm_entrypoint_conf_structure(self,
        conf: Dict[str, Any]
    ):
        """
        At this point, we know that the `entrypoint` key exists and is a
        dictionary. Confirm that the `entrypoint` section of the configuration is
        properly structured

        args:
            conf: agent configuration
        returns:
            True if the `entrypoint` section is properly structured
        raises:
            ValueError() if the `entrypoint` section is not properly structured
        """
        entrypoint = conf["entrypoint"]

        # Only one required value: max_concurrency. This controls how many cloud
        # instances are instantiated at once
        required_keys = [
            ConfigurationKey("type", str, SUPPORTED_ENTRYPOINTS),
            ConfigurationKey("cmd", str),
        ]
        for _k in required_keys:
            _check_key_in_conf(_k, entrypoint, "entrypoint")

        # Projects *must* have a `src` key.
        etype = entrypoint["type"]
        if etype == "project":
            src_key = ConfigurationKey("src", str)
            _check_key_in_conf(src_key, entrypoint, "entrypoint")

        # Functions can have keyword arguments (technically, scripts can have arguments
        # as well, but we would expect these to be reflected in the command).
        if etype == "function":
            fn_key = ConfigurationKey("kwargs", dict)
            _check_optional_key_in_conf(fn_key, entrypoint, "entrypoint")

    def confirm_additional_paths_conf_structure(self,
        conf: Dict[str, Any]
    ):
        """
        If the `additional_paths` section exists (remember, it's an optional key),
        confirm that it is properly structured

        args:
            conf: agent configuration
        returns:
            True if the `additional_paths` section doesn't exist or exists and is
            properly structured
        raises:
            ValueError() if the `additional_paths` section is not properly structured
        """
        optional_key = ConfigurationKey("additional_paths", list)
        _check_optional_key_in_conf(optional_key, conf)
        return True
