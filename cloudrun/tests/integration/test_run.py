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
    s3_file_exists,
    delete_s3_file,
)


# Constants
TEST_DIR = Path(__file__).parent
TEST_FUNCTION = TEST_DIR / 'function'
TEST_JUPYTER = TEST_DIR / 'jupyter'
TEST_PROJECT = TEST_DIR / 'project'
TEST_SCRIPT = TEST_DIR / 'script'


# Tests
def _integration_test(test_path: Path, fname_name: str):
    os.chdir(test_path)
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

    # Delete file in S3, if it exists
    file_s3_uri = f"s3://cloudrun/tests/{fname_name}.txt"
    delete_s3_file(file_s3_uri)

    # Run
    result = runner.invoke(
        cli, ["run", "-f", "cloudrun.yml"]
    )
    assert result.exit_code == 0
    test_output = s3_file_exists(file_s3_uri)
    expected_output = f"Hello world from our `{fname_name}` test case!"
    assert test_output == expected_output

    # Delete the resource
    result = runner.invoke(
        cli, ["delete", "-f", "cloudrun.yml"]
    )
    assert result.exit_code == 0


def test_function():
    """
    Test the output of a function deployment
    """
    _integration_test(TEST_FUNCTION, "test_function")


def test_script():
    """
    Test the output of a function deployment
    """
    _integration_test(TEST_SCRIPT, "test_script")


def test_project():
    """
    Test the output of a function deployment
    """
    _integration_test(TEST_PROJECT, "test_project")
