import os
from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pyxelate import Pal
from pyxelate import Pyx
from skimage import io
from tqdm import tqdm

SAVE_FOLDER = "images/examples/"


def plot(subplots=[], save_as=None, save_name="default.png", fig_h=9):
    """Plotting helper function"""
    fig, ax = plt.subplots(
        int(np.ceil(len(subplots) / 3)), min(3, len(subplots)), figsize=(18, fig_h)
    )
    if len(subplots) == 1:
        ax = [ax]
    else:
        ax = ax.ravel()
    for i, subplot in enumerate(subplots):
        if isinstance(subplot, dict):
            ax[i].set_title(subplot["title"])
            ax[i].imshow(subplot["image"])
        else:
            ax[i].imshow(subplot)
    fig.tight_layout()
    if save_as is not None:
        path = os.path.join(SAVE_FOLDER, save_name)
        plt.savefig(path, transparent=True)
    plt.show()


@dataclass
class Pixelate:
    in_dir:str
    out_dir:str
    


def pixelate_images_in_folder(
    in_dir,
    out_dir,
    image,
    factor=None,
    width=None,
    height=None,
    dither="none",
    depth=1,
    sobel=3,
    svd=False,
):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    palette_image = extract_palette_from_image(image)
    for filename in os.listdir(in_dir):
        in_path = in_dir + "/" + filename
        out_path = out_dir + "/" + filename
        image = np.asarray(Image.open(in_path).convert('RGB'))
        model = Pyx(
            factor=factor,
            width=width,
            height=height,
            palette=palette_image,
            dither=dither,
            depth=depth,
            sobel=sobel,
            svd=svd,
        )
        transformed_image = model.fit_transform(image)
        io.imsave(out_path, transformed_image)


def extract_palette_from_image(image):
    palette_image = np.asarray(Image.open(image).convert("RGB"))
    palette_image_red = palette_image.flatten().reshape(-1, 3)
    palette_image_uniq = np.unique(palette_image_red, axis=0)
    return Pal.from_rgb(palette_image_uniq)


def generate_assets(
    from_dir,
    to_dir,
    items,
    palette_image,
    depth=1,
    sobel=3,
    dither="none",
):
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)

    for item in tqdm(items):
        from_subdir = f'{from_dir}/{item["name"]}'
        to_subdir = f'{to_dir}/{item["name"]}'
        pixelate_images_in_folder(
            from_subdir,
            to_subdir,
            image=palette_image,
            width=item.get("width"),
            height=item.get("height"),
            dither=dither,
            depth=depth,
            sobel=sobel,
        )
