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
        agent_conf: Dict[str, Any]
    ):
        """
        Create agent

        args:
            args: user arguments
            conf_fpath: path to the agent's configuration YAML
        """
        self.args = args
        self.agent_conf = agent_conf
