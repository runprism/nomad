"""
Test cases for BaseTask (and its children)
"""

# Imports
import argparse
from pathlib import Path
from cloudrun.tasks.base import BaseTask
import pytest


# Constants
TEST_DIR = Path(__file__).parent
CONFs = TEST_DIR / 'CONFs'
TEST_FUNCTION = TEST_DIR / 'test_function'
TEST_JUPYTER = TEST_DIR / 'test_jupyter'
TEST_PROJECT = TEST_DIR / 'test_projects'
TEST_SCRIPT = TEST_DIR / 'test_scripts'


# Util functions
def _create_task(path: Path):
    args = argparse.Namespace()
    args.file = str(path)
    args.log_level = 'info'
    args.wkdir = str(CONFs)
    task = BaseTask(args)

    # Task name
    assert task.name == "my_cloud_agent"
    return task


# Tests
def test_normal_conf():
    """
    If `additional_paths` is not a list, throw an error
    """
    task = _create_task(path=(CONFs / 'normal_conf.yml'))
    task.check()

    # Expected configuration
    expected_conf = {
        "type": "ec2",
        "instance_type": "t2.micro",
        "requirements": "requirements.txt",
        "entrypoint": {
            "type": "function",
            "src": "scripts",
            "cmd": "test_fn.print_value",
            "kwargs": {
                "value": "hello world",
            }
        },
        "additional_paths": [
            str(CONFs)
        ],
        "env": {
            "ENV_VAR_1": "VALUE1",
            "ENV_VAR_2": "VALUE2",
        }
    }
    assert expected_conf == task.conf


def test_bad_yml_additional_paths():
    """
    If `additional_paths` is not a list, throw an error
    """
    task = _create_task(path=(CONFs / 'bad_additional_paths.yml'))

    # Run the check
    with pytest.raises(ValueError) as cm:
        task.confirm_additional_paths_conf_structure(task.conf)
    expected_msg = "`additional_paths` is not the correct type...should be a <class 'list'>"  # noqa: E501
    assert expected_msg == str(cm.value)


def test_bad_type():
    """
    If `type` is not currently supported, throw an error
    """
    task = _create_task(path=(CONFs / 'bad_type.yml'))

    # Run the check
    with pytest.raises(ValueError) as cm:
        task.check_conf(task.conf, task.name)
    expected_msg = "Unsupported value `emr` for key `type`"  # noqa: E501
    assert expected_msg == str(cm.value)


def test_no_type():
    """
    If `type` does not exist, throw an error
    """
    task = _create_task(path=(CONFs / 'no_type.yml'))

    # Run the check
    with pytest.raises(ValueError) as cm:
        task.check_conf(task.conf, task.name)
    expected_msg = "`type` not found in `my_cloud_agent`'s configuration!"  # noqa: E501
    assert expected_msg == str(cm.value)


def test_bad_requirements():
    """
    `requirements` should be a string representing the path to the project's
    dependencies. If it isn't, throw an error.
    """
    task = _create_task(path=(CONFs / 'bad_requirements.yml'))

    # Run the check
    with pytest.raises(ValueError) as cm:
        task.check_conf(task.conf, task.name)
    expected_msg = "`requirements` is not the correct type...should be a <class 'str'>"  # noqa: E501
    assert expected_msg == str(cm.value)


def test_bad_env():
    """
    `requirements` should be a dictionary of environment variables. If it isn't, throw
    an error.
    """
    task = _create_task(path=(CONFs / 'bad_env.yml'))

    # Run the check
    with pytest.raises(ValueError) as cm:
        task.check_conf(task.conf, task.name)
    expected_msg = "`env` is not the correct type...should be a <class 'dict'>"  # noqa: E501
    assert expected_msg == str(cm.value)


def test_no_entrypoint():
    """
    If `entrypoint` doesn't exist, throw an error. We parse the actual contents of the
    `entrypoint` dictionary in a separate test module.
    """
    task = _create_task(path=(CONFs / 'no_entrypoint.yml'))

    # Run the check
    with pytest.raises(ValueError) as cm:
        task.check_conf(task.conf, task.name)
    expected_msg = "`entrypoint` not found in `my_cloud_agent`'s configuration!"
    assert expected_msg == str(cm.value)


def test_bad_entrypoint():
    """
    If `entrypoint` doesn't exist, throw an error. We parse the actual contents of the
    `entrypoint` dictionary in a separate test module.
    """
    task = _create_task(path=(CONFs / 'bad_entrypoint.yml'))

    # Run the check
    with pytest.raises(ValueError) as cm:
        task.check_conf(task.conf, task.name)
    expected_msg = "`entrypoint` is not the correct type...should be a <class 'dict'>"
    assert expected_msg == str(cm.value)
