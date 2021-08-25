SAVE_IMAGES = True


import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage.transform import rescale, resize

from pyxelate import Pyx, Pal


def plot(subplots=[], save_as=None, fig_h=9):
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
    if save_as is not None and SAVE_IMAGES:
        # Save image as an example in README.md
        plt.savefig(os.path.join("images/examples/", save_as), transparent=True)
    plt.show()


def pixelate_images_in_folder(
    in_dir,
    out_dir,
    image_model,
    palette,
    factor=None,
    width=None,
    height=None,
    dither="none",
    boost=True,
):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    model = Pyx(
        factor=factor,
        width=width,
        height=height,
        palette=palette,
        dither=dither,
        boost=boost,
    ).fit(image_model)

    print("start")
    for filename in os.listdir(in_dir):
        in_path = in_dir + "/" + filename
        out_path = out_dir + "/" + filename
        image = io.imread(in_path)
        transformed_image = model.transform(image)
        io.imsave(out_path, transformed_image)
    print("done")


def main():
    palette_image = io.imread("images/palettes/retro-115-8x.png")
    palette = 7
    boost = False
    pixelate_images_in_folder(
        "images/top_down_spaceships",
        "images/pixel_top_down_spaceships",
        palette_image,
        palette=palette,
        width=64,
        height=64,
        dither="naive",
        boost=boost,
    )

    pixelate_images_in_folder(
        "images/main_weapons",
        "images/pixel_main_weapons",
        palette_image,
        palette=palette,
        dither="naive",
        boost=boost,
    )

    pixelate_images_in_folder(
        "images/bullets",
        "images/pixel_bullets",
        palette_image,
        palette=palette,
        dither="naive",
        boost=boost,
    )

    pixelate_images_in_folder(
        "images/beam_jet",
        "images/pxel_beam_jet",
        palette_image,
        palette=palette,
        dither="naive",
        boost=boost,
    )
