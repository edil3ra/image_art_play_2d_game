import math
from os import path
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from pyxelate import Pal
from pyxelate import Pyx
from skimage import io
from skimage import color
from lib import plot


# "none", "naive", "bayer", "floyd", "atkinson"
# sobel default 1
# depth default 1

image = np.asarray(Image.open("images/source/platform/Brown tiles/tileBrown_03.png").convert('RGBA'))
# palette_image = np.asarray(Image.open("images/palettes/optimized-grayscale-4-8x.png").convert('RGB'))
# palette_image = np.asarray(Image.open("images/palettes/nyx8-32x.png").convert('RGB'))
# palette_image = Image.open("images/palettes/slso8-32x.png")
# palette_count = 4
# model = Pyx(palette=palette_count,)
# model.fit(palette_image)
# image_transformed = model.transform(image)
# plot([image, image_transformed], True)




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



palette_image = np.asarray(Image.open("images/palettes/nyx8-32x.png").convert('RGB'))
a = palette_image.flatten().reshape(-1, 3)
b = np.unique(a, axis=0)




size = 23
max = 255
min = 0
step = max / size
a = np.array(list([i * step, i * step, i * step] for i in range(0, size+1)), dtype=np.uint8) 
pal = Pal.from_rgb(a)

im = Image.fromarray(a)
im.save('pallete-24.png')   

# model = Pyx(palette=size, dither='bayer', svd=True, sobel=4, depth=2)
model = Pyx(palette=pal, dither="none", svd=True, sobel=2, depth=2)
image_transformed = model.fit_transform(image)
plot([image, image_transformed], True)


