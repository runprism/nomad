"""
Entrypoint into CloudRun
"""


# Importa
import argparse
import rich_click as click
from cloudrun.tasks import (
    apply as apply_task,
    run as run_task,
    delete as delete_task,
)
from pathlib import Path
import os


# Use markup
click.rich_click.USE_MARKDOWN = True


# Construct command
def invoke():
    return cli()


@click.group
def cli():
    pass


@cli.command()
@click.option(
    "--file", "-f",
    type=click.Path,
    help="""CloudRun configuration file""",
    required=True
)
@click.option(
    "--name",
    help="""Name of agent within CloudRun configuration file""",
    required=False
)
@click.option(
    '--log-level', '-l',
    type=click.Choice(['info', 'warn', 'error', 'debug']),
    default="info",
    help="""Set the log level. Default is `info`""",
    required=False
)
def apply(file: str, name: str, log_level: str):
    args = argparse.Namespace()
    args.file = file
    args.name = name
    args.wkdir = Path(os.path.abspath(file)).parent
    args.log_level = log_level

    # Apply task
    task = apply_task.ApplyTask(args)
    return task.run()


@cli.command()
def build():
    pass


@cli.command()
@click.option(
    "--file", "-f",
    type=click.Path,
    help="""CloudRun configuration file""",
    required=True
)
@click.option(
    "--name",
    help="""Name of agent within CloudRun configuration file""",
    required=False
)
@click.option(
    '--log-level', '-l',
    type=click.Choice(['info', 'warn', 'error', 'debug']),
    default="info",
    help="""Set the log level _[default: `info`]_""",
    required=False
)
@click.option(
    '--no-delete',
    is_flag=True,
    default=False,
    help="""Preserve the cloud resources after a successful project run _[default: `False`]_""",  # noqa: E501
    required=False
)
def run(file: str, name: str, log_level: str, no_delete: bool):
    args = argparse.Namespace()
    args.file = file
    args.name = name
    args.wkdir = Path(os.path.abspath(file)).parent
    args.log_level = log_level

    # Apply task
    task = run_task.RunTask(args)
    return task.run()


@cli.command()
@click.option(
    "--file", "-f",
    type=click.Path,
    help="""CloudRun configuration file""",
    required=True
)
@click.option(
    "--name",
    help="""Name of agent within CloudRun configuration file""",
    required=False
)
@click.option(
    '--log-level', '-l',
    type=click.Choice(['info', 'warn', 'error', 'debug']),
    default="info",
    help="""Set the log level _[default is `info`]_""",
    required=False
)
def delete(file: str, name: str, log_level: str):
    args = argparse.Namespace()
    args.file = file
    args.name = name
    args.wkdir = Path(os.path.abspath(file)).parent
    args.log_level = log_level

    # Apply task
    task = delete_task.DeleteTask(args)
    return task.run()
