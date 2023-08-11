"""
Entrypoint into CloudRun
"""


# Importa
import argparse
import rich_click as click
from cloudrun.tasks import (
    apply as apply_task,
    delete as delete_task,
)
from pathlib import Path


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
def apply(file, name):
    args = argparse.Namespace()
    args.file = file
    args.name = name
    args.wkdir = Path.cwd()

    # Apply task
    task = apply_task.ApplyTask(args)
    task.run()


@cli.command()
def build():
    pass


@cli.command()
def run():
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
def delete(file, name):
    args = argparse.Namespace()
    args.file = file
    args.name = name
    args.wkdir = Path.cwd()

    # Apply task
    task = delete_task.DeleteTask(args)
    task.run()
