"""
Basek task class
"""

###########
# Imports #
import argparse
from pathlib import Path
from typing import Any, Dict

# Internal imports
from cloudrun.parsers.yml import YmlParser


# Class definition
class BaseTask:

    def __init__(self,
        args: argparse.Namespace,
    ):
        self.args = args

        # Args will definitely have a `file` attribute
        self.conf_fpath = Path(self.args.file)
        raw_conf = self.parse_conf_fpath(self.conf_fpath)

        # If the user specified a specific agent to use in their args, then use that
        if hasattr(self.args, "name"):
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
