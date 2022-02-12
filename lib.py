SAVE_IMAGES = True


import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from tqdm import tqdm
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
    palette,
    image_model=None,
    factor=None,
    width=None,
    height=None,
    dither="none",
):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    model = None
    if image_model is not None:
        model = Pyx(
            factor=factor,
            width=width,
            height=height,
            palette=palette,
            dither=dither,
        ).fit(image_model)

    for filename in os.listdir(in_dir):
        in_path = in_dir + "/" + filename
        out_path = out_dir + "/" + filename
        image = io.imread(in_path)
        if image_model is None:
            model = Pyx(
                factor=factor,
                width=width,
                height=height,
                palette=palette,
                dither=dither,
            ).fit(image)
        transformed_image = model.transform(image)
        io.imsave(out_path, transformed_image)


def generate_assets(from_dir, to_dir, palette_count, items, palette_image=None, dither="naive"):
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
    
    for item in tqdm(items):
        from_subdir = f'{from_dir}/{item["name"]}'
        to_subdir = f'{to_dir}/{item["name"]}'
        pixelate_images_in_folder(
            from_subdir,
            to_subdir,
            image_model=io.imread(palette_image) if palette_image is not None else None,
            palette=palette_count,
            width=item.get('width'),
            height=item.get('height'),
            dither=dither,
        )


