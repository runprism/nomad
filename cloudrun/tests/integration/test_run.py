"""
Integration tests (i.e., full runs on micro EC2 instances).
"""

# Imports
import os
from pathlib import Path
from click.testing import CliRunner
from cloudrun.main import cli
from cloudrun.tests.integration.utils import (
    key_pair_exists,
    security_group_exists,
    running_instance_exists,
    s3_file_exists
)


# Constants
TEST_DIR = Path(__file__).parent
TEST_FUNCTION = TEST_DIR / 'function'
TEST_JUPYTER = TEST_DIR / 'jupyter'
TEST_PROJECT = TEST_DIR / 'projects'
TEST_SCRIPT = TEST_DIR / 'scripts'


# Tests
def test_function():
    """
    Test the output of a function deployment
    """
    os.chdir(TEST_FUNCTION)
    runner = CliRunner()

    # Invoke the `apply` command
    result = runner.invoke(
        cli, ["apply", "-f", "cloudrun.yml"]
    )

    # Check if EC2 resources exist
    resource_name = "my_cloud_agent"
    assert key_pair_exists(resource_name)
    assert security_group_exists(resource_name)
    assert running_instance_exists(resource_name)
    assert result.exit_code == 0

    # Run
    result = runner.invoke(
        cli, ["run", "-f", "cloudrun.yml"]
    )
    assert result.exit_code == 0
    print(result.output)
    test_output = s3_file_exists("s3://cloudrun/tests/test_function.txt")
    expected_output = "Hello world from our `test_function` test case!"
    assert test_output == expected_output

    result = runner.invoke(
        cli, ["delete", "-f", "cloudrun.yml"]
    )
