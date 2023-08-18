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
from typing import List


# Constants
TEST_DIR = Path(__file__).parent
TEST_FUNCTION = TEST_DIR / 'function'
TEST_JUPYTER = TEST_DIR / 'jupyter'
TEST_PROJECT = TEST_DIR / 'project'
TEST_SCRIPT = TEST_DIR / 'script'


# Tests
def _resources_exist(resource_name: str):
    return {
        "key_pair": key_pair_exists(resource_name),
        "security_group": security_group_exists(resource_name),
        "instance": running_instance_exists(resource_name)
    }


def _apply_run_integration_test(
    test_path: Path,
    fname_name: str,
    run_args: List[str]
):
    os.chdir(test_path)
    runner = CliRunner()

    # Invoke the `apply` command
    result = runner.invoke(cli, ["apply", "-f", "cloudrun.yml"])

    # Check if EC2 resources exist
    resource_name = "my_cloud_agent"
    resources = _resources_exist(resource_name)
    assert resources["key_pair"]
    assert resources["security_group"]
    assert resources["instance"]
    assert result.exit_code == 0

    # Delete file in S3, if it exists
    file_s3_uri = f"s3://cloudrun/tests/{fname_name}.txt"
    delete_s3_file(file_s3_uri)

    # Run
    result = runner.invoke(cli, run_args)
    assert result.exit_code == 0
    test_output = s3_file_exists(file_s3_uri)
    expected_output = f"Hello world from our `{fname_name}` test case!"
    assert test_output == expected_output


def test_function():
    """
    Test the output of a function deployment
    """
    _apply_run_integration_test(
        TEST_FUNCTION,
        "test_function",
        ['run', '-f', 'cloudrun.yml', '--no-delete-success']
    )

    # The resources should still exist.
    resource_name = "my_cloud_agent"
    resources = _resources_exist(resource_name)
    assert resources["key_pair"]
    assert resources["security_group"]
    assert resources["instance"]

    # Run, but this time put delete on success
    runner = CliRunner()
    result = runner.invoke(cli, ['run', '-f', 'cloudrun.yml'])
    assert result.exit_code == 0
    resources = _resources_exist(resource_name)
    assert not resources["key_pair"]
    assert not resources["security_group"]
    assert not resources["instance"]


def test_script():
    """
    Test the output of a function deployment
    """
    _apply_run_integration_test(
        TEST_SCRIPT,
        "test_script",
        ['run', '-f', 'cloudrun.yml', '--no-delete-success']
    )

    # The resources should still exist.
    resource_name = "my_cloud_agent"
    resources = _resources_exist(resource_name)
    assert resources["key_pair"]
    assert resources["security_group"]
    assert resources["instance"]

    # Run, but this time put delete on success
    runner = CliRunner()
    result = runner.invoke(cli, ['run', '-f', 'cloudrun.yml'])
    assert result.exit_code == 0
    resources = _resources_exist(resource_name)
    assert not resources["key_pair"]
    assert not resources["security_group"]
    assert not resources["instance"]


def test_project():
    """
    Test the output of a function deployment
    """
    _apply_run_integration_test(
        TEST_PROJECT,
        "test_project",
        ['run', '-f', 'cloudrun.yml', '--no-delete-success']
    )

    # The resources should still exist.
    resource_name = "my_cloud_agent"
    resources = _resources_exist(resource_name)
    assert resources["key_pair"]
    assert resources["security_group"]
    assert resources["instance"]

    # Run, but this time put delete on success
    runner = CliRunner()
    result = runner.invoke(cli, ['run', '-f', 'cloudrun.yml'])
    assert result.exit_code == 0
    resources = _resources_exist(resource_name)
    assert not resources["key_pair"]
    assert not resources["security_group"]
    assert not resources["instance"]
