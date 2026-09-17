from MLX.libmlx import *
from MLXCanvas import MlxCanvas
from GridConfig import GridConfig
from GridMaker import GridMaker

from PIL import Image
from typing import Dict, Tuple
import os


import ctypes


class mlx_layers(ctypes.Structure):
    _fields_ = [
        ("text_layer", ctypes.POINTER(mlx_image_t)),
        ("draw_layer", ctypes.POINTER(mlx_image_t)),
        ("grid_layer", ctypes.POINTER(mlx_image_t)),
    ]

@mlx_loop_hook_func
def handel_input(param: int) -> None:
    mlx_ptr = ctypes.cast(param, ctypes.POINTER(mlx_t))

    if (mlx.mlx_is_key_down(mlx_ptr, MLX_KEY_E)):
        os._exit(0)
    pass

@mlx_mousefunc
def mouse_hook(button, x, y, param) -> None:
    mlx_ptr = ctypes.cast(param, ctypes.POINTER(mlx_t))

    x = ctypes.c_uint32(0)
    y = ctypes.c_uint32(0)

    mlx.mlx_get_mouse_pos(mlx_ptr, ctypes.byref(x), ctypes.byref(y))

    if (button == 0):
        MlxCanvas._draw_circle(layers.draw_layer, x.value, y.value, 50)


if __name__ == "__main__":
    grid_config: GridConfig = GridConfig._from_file("./config.toml")

    mlx_ptr = mlx.mlx_init(grid_config.w,
                           grid_config.h, b"Graph Grid", False)

    layers = mlx_layers()

    layers.text_layer = mlx.mlx_new_image(mlx_ptr, grid_config.w, grid_config.h)
    layers.grid_layer = mlx.mlx_new_image(mlx_ptr, grid_config.w, grid_config.h)
    layers.draw_layer = mlx.mlx_new_image(mlx_ptr, grid_config.w, grid_config.h)



    mlx.mlx_image_to_window(mlx_ptr, layers.grid_layer, 0, 0)
    mlx.mlx_image_to_window(mlx_ptr, layers.text_layer, 0, 0)
    mlx.mlx_image_to_window(mlx_ptr, layers.draw_layer, 0, 0)

    MlxCanvas._fill_mlximg_by_color(layers.grid_layer, 0xffffffff)

    GridMaker._create_graph_grid(layers.grid_layer, layers.text_layer,
                                 0, 0, grid_config.w, grid_config.h,
                                 grid_config)


    mlx.mlx_loop_hook(mlx_ptr, handel_input, ctypes.cast(mlx_ptr, c_void_p))
    mlx.mlx_mouse_hook(mlx_ptr, mouse_hook, ctypes.cast(mlx_ptr, c_void_p))
    mlx.mlx_loop(mlx_ptr)
    pass
