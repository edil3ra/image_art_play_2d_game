import click
import os
import yaml
from lib import generate_assets
import subprocess


root_dir = os.path.dirname(__file__)
default_data_directory = os.path.join(root_dir, 'data')
default_created_directory = os.path.join(root_dir, 'images', 'created')

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    pass


@cli.command()
@click.option('--directory', '-d', default=None)
def template(directory):
    '''list templates to create art assets'''
    if directory is None:
        directory = default_data_directory
    list_directory(directory)

    

@cli.command()
@click.option('--directory', '-d', default=None)
def created(directory):
    '''list created assets from templates'''
    if directory is None:
        directory = os.path.join(root_dir, default_created_directory)
    list_directory(directory)


@cli.command()
@click.option('--name', '-n', required=True)
def generate(name):
    '''Generate assets from template name'''
    data = yaml.full_load(open(os.path.join(default_data_directory, f'{name}.yaml')).read())
    generate_assets(**data)


@cli.command()
@click.option('--name', '-n', required=True)
@click.option('--to', '-t', required=True)
def copy(name, to):
    '''copy created assets to given directory'''
    path = os.path.join(default_created_directory, name)
    subprocess.run(['cp', '-r', path, to])
    


def list_directory(directory):
    files = os.listdir(directory)
    basenames = [file.split('.')[0] for file in files]
    fullnames= [os.path.abspath(os.path.join(directory, file))  for file in files]
    paths = ['{} - {}'.format(basename, fullname) for (basename, fullname) in zip(basenames, fullnames)]
    click.echo('\n'.join(paths))

    
if __name__ == '__main__':
    cli(obj={})

