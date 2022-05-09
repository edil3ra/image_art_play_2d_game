import os
from dataclasses import dataclass
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pyxelate import Pal
from pyxelate import Pyx
from skimage import io
from tqdm import tqdm

from types_pyxelate import Config
from types_pyxelate import Item
from types_pyxelate import Palette

SAVE_FOLDER = "images/examples/"


@dataclass
class Pixelate:
    in_dir: str
    out_dir: str


def pixelate_images_in_folder(
    in_dir: str,
    out_dir: str,
    palette_dir: str,
    palettes: List[Palette],
    width=32,
    height=32,
    dither="none",
    depth=1,
    sobel=3,
    svd=False,
):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # palette_image = extract_palette_from_image(image)
    for filename in os.listdir(in_dir):
        transformed_image = None
        in_path = in_dir + "/" + filename
        out_path = out_dir + "/" + filename
        for palette in palettes:
            image_palette = extract_palette_from_image(
                os.path.join(palette_dir, palette.name)
            )
            if transformed_image is None:
                transformed_image = np.asarray(Image.open(in_path).convert("RGB"))
            model = Pyx(
                width=width,
                height=height,
                palette=palette.size,
                dither=dither,
                depth=depth,
                sobel=sobel,
                svd=svd,
            )
            transformed_image = model.fit_transform(transformed_image)
        io.imsave(out_path, transformed_image)


def extract_palette_from_image(image):
    palette_image = np.asarray(Image.open(image).convert("RGB"))
    palette_image_red = palette_image.flatten().reshape(-1, 3)
    palette_image_uniq = np.unique(palette_image_red, axis=0)
    return Pal.from_rgb(palette_image_uniq)


def generate_assets(config: Config):
    if not os.path.exists(config.destination_dir):
        os.makedirs(config.destination_dir)

    for item in tqdm(config.items):
        source_subdir = f"{config.source_dir}/{item.name}"
        destination_subdir = f"{config.destination_dir}/{item.name}"
        pixelate_images_in_folder(
            source_subdir,
            destination_subdir,
            config.palette_dir,
            palettes=item.palettes,
            width=item.width,
            height=item.height,
            dither=config.dither,
            depth=config.depth,
            sobel=config.sobel,
        )
