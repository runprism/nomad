"""
Test cases for base task
"""

# Imports
import argparse
from cloudrun.examples import EXAMPLES_DIR
from cloudrun.tasks.base import BaseTask


# Constants
EC2_EXAMPLES_DIR = EXAMPLES_DIR / 'ec2'
EC2_EXAMPLES = [
    EC2_EXAMPLES_DIR / 'additional_paths.yml',
    EC2_EXAMPLES_DIR / 'basic_function.yml',
    EC2_EXAMPLES_DIR / 'basic_project.yml',
    EC2_EXAMPLES_DIR / 'basic_script.yml',
    EC2_EXAMPLES_DIR / 'env_vars.yml',
]


# Tests
def test_ec2_examples():
    tasks = []
    for _p in EC2_EXAMPLES:

        # Create task
        args = argparse.Namespace()
        args.file = _p
        args.wkdir = EC2_EXAMPLES_DIR
        print(_p)
        task = BaseTask(args)

        # All of the tasks should only have one agent
        assert task.name == "my_cloud_agent"

        tasks.append(task)
