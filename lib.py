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
    image_model,
    palette,
    factor=None,
    width=None,
    height=None,
    dither="none",
    boost=False,
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

    for filename in os.listdir(in_dir):
        in_path = in_dir + "/" + filename
        out_path = out_dir + "/" + filename
        image = io.imread(in_path)
        transformed_image = model.transform(image)
        io.imsave(out_path, transformed_image)


def generate_assets(from_dir, to_dir, palette_image, palette_count, items, dither="naive", boost=False):
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
    
    for item in tqdm(items):
        from_subdir = f'{from_dir}/{item["name"]}'
        to_subdir = f'{to_dir}/{item["name"]}'
        pixelate_images_in_folder(
            from_subdir,
            to_subdir,
            image_model=io.imread(palette_image),
            palette=palette_count,
            width=item.get('width'),
            height=item.get('height'),
            dither=dither,
            boost=boost,
        )


    

        
# def generate_shooter_game():
#     from_main_dir = "images/normal"
#     to_main_dir = "images/pixelate"
#     palette_image = io.imread("images/palettes/mulfok32-32x.png")
#     palette = 16
#     boost = True
#     subdirs = [
#         ("special_units", 64, 64),
#         ("overloadMonster", 64, 64),
#         ("top_down_spaceships", 64, 64),
#         ("simple_explosion", 64, 64),
#         ("sonic_explosion", 64, 64),
#         ("filled", None, None),
#         ("laser_beams", None, None),
#         ("bullets", None, None),
#         ("spaceBackground", None, None),
#         ("stars", None, None),
#         ("main_weapons", None, None),
#         ("beam_jet", None, None),
#     ]

#     for (dir, width, height) in tqdm(subdirs):
#         from_dir = f'{from_main_dir}/{dir}'
#         to_dir = f'{to_main_dir}/{dir}'
        
#         pixelate_images_in_folder(
#             from_dir,
#             to_dir,
#             palette_image,
#             palette=palette,
#             width=width,
#             height=height,
#             dither="naive",
#             boost=boost,
#         )



# def main():
#     generate_shooter_game()


# if __name__ == '__main__':
#     main()
