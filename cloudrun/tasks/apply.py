"""
Task called via the `cloudrun apply` CLI command
"""


# Imports
from cloudrun.agents.base import Agent
from cloudrun.agents.meta import MetaAgent
from cloudrun.agents import meta  # noqa
from cloudrun.tasks.base import BaseTask


# Class definition
class ApplyTask(BaseTask):

    def run(self):
        """
        Create the agent specified in the user's configuration file
        """
        agent_type = self.conf["type"]
        agent: Agent = MetaAgent.get_agent(agent_type)(
            args=self.args,
            agent_conf=self.conf,
        )
        agent.apply()
