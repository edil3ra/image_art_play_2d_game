from typing import List
from typing import Literal
from typing import Optional

from pydantic import BaseModel

DEFAULT_DEPTH = 1
DEFAULT_SOBEL = 3
DEFAULT_DITHER = "none"
DEFAULT_SVD = True
DEFAULT_ALPHA = 0.6


Dither = Literal["none", "naive", "bayer", "floyd", "atkinson"]


class Palette(BaseModel):
    name: str
    size: int


class Item(BaseModel):
    name: str
    width: Optional[int]
    height: Optional[int]
    palettes: List[Palette]


class Main(BaseModel):
    source_dir: str
    destination_dir: str
    palette_dir: str
    dither: Dither = DEFAULT_DITHER
    depth = DEFAULT_DEPTH
    sobel = DEFAULT_SOBEL
    svd = DEFAULT_SVD
    alpha = DEFAULT_ALPHA
    items: List[Item]



