"""
Task called via the `cloudrun delete` CLI command
"""


# Imports
from cloudrun.agents.base import Agent
from cloudrun.agents.meta import MetaAgent
from cloudrun.agents import (  # noqa: F401
    meta,
    ec2,
)
from cloudrun.tasks.base import BaseTask


# Class definition
class DeleteTask(BaseTask):

    def run(self):
        """
        Create the agent specified in the user's configuration file
        """
        self.check()
        agent_type = self.conf["type"]
        agent: Agent = MetaAgent.get_agent(agent_type)(
            args=self.args,
            cloudrun_wkdir=self.cloudrun_wkdir,
            agent_name=self.name,
            agent_conf=self.conf,
            entrypoint=self.entrypoint,
        )
        return agent.delete()
