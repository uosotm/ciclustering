#!/usr/bin/env python3
#-*-coding:utf-8-*-

import base64
import configparser
import click
import csv
import glob
import json
import pathlib
import requests
import shutil
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
    config_path = pathlib.Path(value)
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

def ensure_dir(path):
    try:
        path.mkdir(parents=True, exist_ok=True)
    except FileExistsError as e:
        click.secho('Error: {} isn\'t directory'.format(e),
                    fg='red', err=True)
        sys.exit(1)

def encode_image(image):
    image_content = image.read()
    return base64.b64encode(image_content).decode('UTF-8')

def create_request(encoded_image, mode):
    request_list = []
    content_json_obj = {
        'content': encoded_image
    }

    feature_json_obj = []
    if mode == 'object':
        feature_json_obj.append({
            'type': 'LABEL_DETECTION',
            'maxResults': 10
        })
    else:
        feature_json_obj.append({
            'type': 'FACE_DETECTION'
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
              expose_value=False, is_eager=True,
              help='Print version.')
@click.option('--config', callback=load_config,
              default=(str(pathlib.Path.home() / '.ciclustering')),
              help='Path to config file.')
@click.option('--dest', default='dest',
              help='Path to output files.')
@click.option('--mode', type=click.Choice(['object', 'human']),
              default='object', help='Specify recognition mode')
@click.argument('images_path')
def main(config, dest, mode, images_path):
    """CI clustering is an automation tool for Collective Idea"""

    # Initialize recognition mode
    if mode == 'object':
        keyword = click.prompt('Please enter a keyward')

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
        dest_keyword = dest / keyword
        dest_others = dest / 'others'
        try:
            dest.mkdir(parents=True, exist_ok=True)
            dest_keyword.mkdir(parents=True, exist_ok=True)
            dest_others.mkdir(parents=True, exist_ok=True)

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

        with (dest / 'results.csv').open('w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')

            for image in tqdm(images, desc='Recognising', total=length, ncols=10):
                row = [str(image)]
                with image.open('rb') as imagefile:
                    encoded_image = encode_image(imagefile)

                payload = create_request(encoded_image, mode)
                res = upload(cva_url, cva_key, payload)

                # Organize files to proper directory 
                try:
                    labels = json.loads(res)['responses'][0]['labelAnnotations']
                except KeyError:
                    writer.writerow(row)
                    continue

                descriptions = [label['description'] for label in labels]
                scores = [label['score'] for label in labels]
                if keyword in descriptions:
                    shutil.move(str(image), str(dest_keyword))
                else:
                    shutil.move(str(image), str(dest_others))

                for name, score in zip(descriptions, scores):
                    row.append('{}({})'.format(name, score))

                writer.writerow(row)

    else:
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

        with (dest / 'results.csv').open('w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')

            for image in tqdm(images, desc='Recognising', total=length, ncols=10):
                row = [str(image)]
                with image.open('rb') as imagefile:
                    encoded_image = encode_image(imagefile)

                payload = create_request(encoded_image, mode)
                res = upload(cva_url, cva_key, payload)

                # Organize files to proper directory 
                try:
                    faces = len(json.loads(res)['responses'][0]['faceAnnotations'])
                except KeyError:
                    faces = 0

                dest_number = pathlib.Path(dest) / str(faces)
                try:
                    dest_number.mkdir(parents=True, exist_ok=True)
                except FileExistsError:
                    click.secho('Error: {} isn\'t directory'.format(dest_number.resolve()),
                                fg='red', err=True)
                    sys.exit(1)

                shutil.move(str(image), str(dest_number))
                row.append('{}'.format(faces))
                writer.writerow(row)


    click.secho('Done!', bold=True, fg='green')
