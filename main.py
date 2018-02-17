import base64
import configparser
import click
import glob
import pathlib
import requests
import sys
import time
import urllib
from datetime import datetime
from tqdm import tqdm


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 0.1.0')
    ctx.exit()

def load_config(ctx, param, value):
    config_path = value
    config = configparser.ConfigParser()

    if not config_path.exists():
        click.echo('Couldn\'t find ({}) to get config.'.format(config_path))
        if click.confirm('Would you like to create a new config there?'):  
            new_config(config_path, config)
            ctx.exit('Please run the command again.')
        else:
            ctx.exit('Exit.')

    config.read(str(config_path), encoding='utf8')
    return config

def new_config(config_path, config):
    cva_url = click.prompt('\nRequests to',
            default='https://vision.googleapis.com/v1/images:annotate')
    cva_key = click.prompt('Please enter your API KEY')
    config['default'] = { 'cva_url': cva_url,
                          'cva_key': cva_key }

    with config_path.open('w') as configfile:
        config.write(configfile)
        click.echo('\nSaving config...')

    click.secho('Successfuly created the config file!',
            bold=True, fg='green')

def encode_image(image):
    image_content = image.read()
    return base64.b64encode(image_content).decode('UTF-8')

def create_request(encoded_image):
    request_list = []
    content_json_obj = {
        'content': encoded_image
    }

    feature_json_obj = []
    feature_json_obj.append({
        'type': 'LABEL_DETECTION',
        'maxResults': 10
    })

    request_list.append({
        'features': feature_json_obj,
        'image': content_json_obj,
    })
    return { 'requests': request_list }

def upload(url, key, data):
    args = { 'key': key }
    url = url + "?{}".format(urllib.parse.urlencode(args))
    r = requests.post(url, json=data)
    return r.text


@click.command()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help='Print version.')
@click.option('--config', callback=load_config,
              default=(pathlib.Path.home() / '.ciclustering'),
              help='Path to config file.')
@click.option('--dest', default='dest', help='Path to output files.')
@click.argument('images_path')
def cli(config, dest, images_path):
    """CI clustering is an automation tool for Collective Idea"""

    # Validate path to images
    images_path = pathlib.Path(images_path)
    if not images_path.exists():
        click.secho('Error: No such directory',
                    fg='red', err=True) 
        sys.exit(1)

    if not images_path.is_dir():
        click.secho('Error: {} isn\'t directory'.format(str(images_path)),
                    fg='red', err=True)
        sys.exit(1)

    click.echo('Path to target directory: {}'.format(images_path.resolve()))

    # Validate and create a directory for output files
    dest = pathlib.Path(dest)
    try:
        dest.mkdir(parents=True, exist_ok=True)

    except FileExistsError:
        click.secho('Error: {} isn\'t directory'.format(dest.resolve()),
                    fg='red', err=True)
        sys.exit(1)
    click.echo('Created a directory for results: {}'.format(dest.resolve()))
    
    # Count only jpg images in path
    images = [image for image in images_path.glob('*.jpg')]
    length = len(images)
    click.echo('Reading files for process: {} media\n'.format(length))

    cva_url = config['default']['cva_url']
    cva_key = config['default']['cva_key']

    for image in tqdm(images, desc='Recognising', total=length, ncols=10):
        with image.open('rb') as imagefile:
            encoded_image = encode_image(imagefile)
            payload = create_request(encoded_image)
            res = upload(cva_url, cva_key, payload)
            print(res)

    click.secho('Done!', bold=True, fg='green')
