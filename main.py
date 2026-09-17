from MLX.libmlx import *
from MLXCanvas import MlxCanvas
from GridConfig import GridConfig
from GridMaker import GridMaker

from PIL import Image
from typing import Dict, Tuple
import os


import ctypes


@mlx_loop_hook_func
def handel_input(param: int) -> None:
    mlx_ptr = ctypes.cast(param, ctypes.POINTER(mlx_t))

    if (mlx.mlx_is_key_down(mlx_ptr, MLX_KEY_E)):
        os._exit(0)
    pass


if __name__ == "__main__":
    grid_config: GridConfig = GridConfig._from_file("./config.toml")

    print("width: ", grid_config.w)
    print("height: ", grid_config.h)
    print("grid size: ", grid_config.grid_size)

    mlx_ptr = mlx.mlx_init(grid_config.w,
                           grid_config.h, b"Graph Grid", False)

    gridlayer = mlx.mlx_new_image(mlx_ptr, grid_config.w, grid_config.h)
    text_layer = mlx.mlx_new_image(mlx_ptr, grid_config.w, grid_config.h)


    mlx.mlx_image_to_window(mlx_ptr, gridlayer, 0, 0)
    mlx.mlx_image_to_window(mlx_ptr, text_layer, 0, 0)

    MlxCanvas._fill_mlximg_by_color(gridlayer, 0xffffffff)

    GridMaker._create_graph_grid(gridlayer, text_layer, 0, 0, grid_config.w, grid_config.h, 0x000000ff, grid_config.grid_size)


    mlx.mlx_loop_hook(mlx_ptr, handel_input, ctypes.cast(mlx_ptr, c_void_p))
    mlx.mlx_loop(mlx_ptr)
    pass
