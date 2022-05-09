import os

import yaml

from lib import generate_assets
from lib import pixelate_images_in_folder
from types_pyxelate import Config

root_dir = os.path.dirname(".")
default_data_directory = os.path.join(root_dir, "data")

config = Config.parse_obj(
    yaml.full_load(open(os.path.join(default_data_directory, "platform.yaml")).read())
)

generate_assets(config)
