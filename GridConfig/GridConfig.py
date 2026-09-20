import tomllib
from pydantic import BaseModel

class GridConfig(BaseModel):
    w: int = 600
    h: int = 420


    axis_color    : int = 0x000000ff
    grid_color    : int = 0x000000ff
    bg_color      : int = 0xffffffff
    text_color    : int = 0x000000ff
    point_color   : int = 0x00ff00ff
    line_color    : int = 0x000000ff

    grid_size     : int = 50
    line_thickness: int = 0
    x_pad         : int = 50
    y_pad         : int = 50

    @staticmethod
    def _from_file(file: str) -> "GridConfig":
        with open(file, 'rb') as f:
            config = tomllib.load(f)


        return GridConfig(**config["grid"])



