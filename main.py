import click
import os
import yaml
from lib import generate_assets

current_dir = os.path.dirname(__file__)
default_directory = 'data'

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")

@cli.command()
@click.option('--directory', '-d', default=None)
def list(directory):
    if directory is None:
        directory = os.path.join(current_dir, default_directory)
    files = os.listdir(directory)
    basenames = [file.split('.')[0] for file in files]
    fullnames= [os.path.abspath(os.path.join(directory, file))  for file in files]
    paths = ['{} - {}'.format(basename, fullname) for (basename, fullname) in zip(basenames, fullnames)]
    click.echo('\n'.join(paths))


@cli.command()
@click.option('--filename', '-f', required=True)
def generate(filename):
    data = yaml.full_load(open(filename).read())
    click.echo(data)
    generate_assets(**data)
    


    

if __name__ == '__main__':
    cli(obj={})

