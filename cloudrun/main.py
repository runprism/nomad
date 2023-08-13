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


# Construct command
def invoke():
    cli()


@click.group
def cli():
    pass


@cli.command()
@click.option(
    "--file", "-f",
    type=str,
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
    help="""Set the log level""",
    required=False
)
def apply(file, name, log_level):
    args = argparse.Namespace()
    args.file = file
    args.name = name
    args.wkdir = Path(os.path.abspath(file)).parent
    args.log_level = log_level

    # Apply task
    task = apply_task.ApplyTask(args)
    task.run()


@cli.command()
def build():
    pass


@cli.command()
@click.option(
    "--file", "-f",
    type=str,
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
    help="""Set the log level""",
    required=False
)
def run(file, name, log_level):
    args = argparse.Namespace()
    args.file = file
    args.name = name
    args.wkdir = Path(os.path.abspath(file)).parent
    args.log_level = log_level

    # Apply task
    task = run_task.RunTask(args)
    task.run()


@cli.command()
@click.option(
    "--file", "-f",
    type=str,
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
    help="""Set the log level""",
    required=False
)
def delete(file, name, log_level):
    args = argparse.Namespace()
    args.file = file
    args.name = name
    args.wkdir = Path(os.path.abspath(file)).parent
    args.log_level = log_level

    # Apply task
    task = delete_task.DeleteTask(args)
    task.run()
