"""
Users can run their code on cloud environments, which we call Agents. This script
contains the base class for the agent.
"""


###########
# Imports #
###########

# Internal imports
from cloudrun.agents.meta import MetaAgent

# Standard library imports
import argparse
from typing import Any, Dict
from pathlib import Path


####################
# Class definition #
####################

class Agent(metaclass=MetaAgent):
    """
    The `agents.yml` file will be formatted as follows:

    agents:
      <agent name here>:
        type: docker
        ...
    """

    def __init__(self,
        args: argparse.Namespace,
        cloudrun_wkdir: Path,
        agent_name: str,
        agent_conf: Dict[str, Any],
        mode: str = "prod"
    ):
        """
        Create agent

        args:
            args: user arguments
            agent_conf: agent configuration as a dictionary
            mode: either `prod` of `test`. This allows us to test agents without
                instantiating cloud resources
        """
        self.args = args
        self.cloudrun_wkdir = cloudrun_wkdir
        self.agent_name = agent_name
        self.agent_conf = agent_conf

        # Check the configuration
        self.check_conf(self.agent_conf)

    def check_conf(self, conf: Dict[str, Any]):
        return True
