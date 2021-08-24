import os
from skimage import io
from pyxelate import Pyx, Pal

def pixelate_images_in_folder(in_dir, out_dir, palette, size, sensitivity_multiplier):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for filename in os.listdir(in_dir):
        in_path = in_dir + '/' + filename
        out_path = out_dir + '/' + filename   
        y=pixelator(
            in_path=in_path,
            palette=palette,
            size=size,
            sensitivity_multiplier=sensitivity_multiplier
        )    

        y.resize_out_img().save_out_img(path=out_path, overwrite=True)



palette = [
    (45,  50,  50),  #black
    (240, 68,  64),  #red
    (211, 223, 223), #white
    (160, 161, 67),  #green
    (233, 129, 76),  #orange
]

pixelate_images_in_folder('images/special_units', 'images/pixel_special_units', palette, (20, 20), 10)


input.resize((10, 10), Image.BICUBIC).quantize()
