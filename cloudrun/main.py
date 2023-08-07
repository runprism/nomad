"""
Entrypoint into CloudRun
"""


# Importa
import rich_click as click


# Construct command
def invoke():
    cli()


@click.group
def cli():
    pass


@cli.command()
def apply():
    pass


@cli.command()
def build():
    pass


@cli.command()
def run():
    pass
