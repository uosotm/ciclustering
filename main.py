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

    # Validat path to images
    images_path = pathlib.Path(images_path)
    if not images_path.exists():
        click.secho('Error: No such directory', fg='red') 
        sys.exit(1)

    if not images_path.is_dir():
        click.secho('Error: {} isn\'t directory'.format(str(images_path)), fg='red')
        sys.exit(1)

    click.echo('Path to input files: {}'.format(images_path.resolve()))

    # TODO: Validate and create a directory for output files
    
    # Count only jpg images in path
    images = [image for image in images_path.glob('*.jpg')]
    click.echo('Reading files for process: {} media'.format(len(images)))

    # TODO: Add progress bar to show image rcognition progress
    for image in images:
        click.echo(image)

    click.secho('Done!', bold=True, fg='green')
