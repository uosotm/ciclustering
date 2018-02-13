import click
import glob
import pathlib
import sys
import time
from datetime import datetime
from tqdm import tqdm


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 0.1.0')
    ctx.exit()

@click.command()
@click.option('--version', is_flag=True, callback=print_version,
        expose_value=False, is_eager=True, help='Print version.')
@click.option('--dest', default='dest', help='Path to output files.')
@click.argument('images_path')
def cli(dest, images_path):
    """CI clustering is an automation tool for Collective Idea"""

    # Validate path to images
    images_path = pathlib.Path(images_path)
    if not images_path.exists():
        click.secho('Error: No such directory', fg='red') 
        sys.exit(1)

    if not images_path.is_dir():
        click.secho('Error: {} isn\'t directory'.format(str(images_path)), fg='red')
        sys.exit(1)

    click.echo('Path to target directory: {}'.format(images_path.resolve()))

    # Validate and create a directory for output files
    dest = pathlib.Path(dest)
    try:
        dest.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        click.secho('Error: {} isn\'t directory'.format(dest.resolve()), fg='red')
        sys.exit(1)
    click.echo('Created a directory for results: {}'.format(dest.resolve()))
    
    # Count only jpg images in path
    images = [image for image in images_path.glob('*.jpg')]
    length = len(images)
    click.echo('Reading files for process: {} media'.format(length))

    for image in tqdm(images, desc='Recognising', total=length, ncols=100):
        # Recognising code goes here.
        time.sleep(0.1)

    click.secho('Done!', bold=True, fg='green')
