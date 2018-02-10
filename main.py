import click
import glob
import pathlib
import sys
import time
from datetime import datetime


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 0.1.0')
    ctx.exit()

@click.command()
@click.option('--version', is_flag=True, callback=print_version,
        expose_value=False, is_eager=True, help='Display version.')
@click.option('--dest', default='dest', help='Path to output files.')
@click.argument('images_path')
def cli(dest, images_path):
    """CIclustering is an automation tool for Collective Idea"""

    images_path = pathlib.Path(images_path)

    if not images_path.exists():
        click.secho('Error: No such directory', fg='red') 
        sys.exit(1)

    if not images_path.is_dir():
        click.secho('Error: {} isn\'t directory'.format(str(images)), fg='red')
        sys.exit(1)

    click.echo('Path to input files: {}'.format(images_path.resolve()))

    images = images_path.glob('*.jpg')
    length = sum(1 for image in images)
    click.echo('Reading files for process: {} media'.format(length))

    for image in images:
        click.echo(image)

    click.secho('Done!', bold=True, fg='green')
