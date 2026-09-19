from MLX.libmlx import *
from MLXCanvas import MlxCanvas
from GridConfig import GridConfig
from GridMaker import GridMaker
from LineDrawing import LineDrawing

from enum import Enum
from PIL import Image
from typing import Dict, Tuple, List

import os
import ctypes


class DrawState(Enum):
    START_POINT  = 1
    END_POINT    = 2
    LINE_DRAWING = 3
    ERASE        = 4

class mlx_layers(ctypes.Structure):
    _fields_ = [
        ("text_layer", ctypes.POINTER(mlx_image_t)),
        ("draw_layer", ctypes.POINTER(mlx_image_t)),
        ("grid_layer", ctypes.POINTER(mlx_image_t)),
    ]


DRAW_STATE   : DrawState  = DrawState.START_POINT
START_POINT  : List[int]  = [0, 0]
END_POINT    : List[int]  = [0, 0]

MOUSE_CLICKED: int        = 0
LAYERS       : mlx_layers = mlx_layers()


@mlx_loop_hook_func
def handel_input(param: int) -> None:
    mlx_ptr = ctypes.cast(param, ctypes.POINTER(mlx_t))

    if (mlx.mlx_is_key_down(mlx_ptr, MLX_KEY_E)):
        os._exit(0)


@mlx_mousefunc
def mouse_event(button, x, y, param) -> None:
    mlx_ptr = ctypes.cast(param, ctypes.POINTER(mlx_t))
    x = ctypes.c_uint32(0)
    y = ctypes.c_uint32(0)

    global MOUSE_CLICKED
    if not MOUSE_CLICKED:
        MOUSE_CLICKED = 1
        return
    else:
        MOUSE_CLICKED = 0

    mlx.mlx_get_mouse_pos(mlx_ptr, ctypes.byref(x), ctypes.byref(y))

    print(x.value, y.value)
    if (button == 0):
        global DRAW_STATE
        if DRAW_STATE != DrawState.ERASE:
            MlxCanvas._draw_circle(LAYERS.draw_layer, x.value, y.value, 5, 0x1E00FFFF)
            if (DRAW_STATE == DrawState.START_POINT):
                START_POINT[0] = x.value
                START_POINT[1] = y.value
                DRAW_STATE = DrawState.END_POINT
            elif (DRAW_STATE == DrawState.END_POINT):
                END_POINT[0] = x.value
                END_POINT[1] = y.value
                DRAW_STATE = DrawState.LINE_DRAWING
                # drawing line here
                LineDrawing.drawLine(LAYERS.draw_layer,
                                     START_POINT[0], START_POINT[1],
                                     END_POINT[0], END_POINT[1], 5,
                                     0xDE06C1FF)
                DRAW_STATE = DrawState.START_POINT

    elif (button == 1):
        DRAW_STATE = DrawState.START_POINT
        LAYERS.draw_layer = MlxCanvas._erase_mlximg(mlx_ptr, LAYERS.draw_layer)

def init_grid_window(grid_config: GridConfig) -> mlx_t:

    window_width = grid_config.w + (grid_config.x_pad * 2)
    window_height = grid_config.h + (grid_config.y_pad * 2)

    mlx_ptr = mlx.mlx_init(window_width,
                           window_height, b"Graph Grid", True)

    LAYERS.text_layer = MlxCanvas._mlx_new_layer(mlx_ptr)
    LAYERS.grid_layer = MlxCanvas._mlx_new_layer(mlx_ptr)
    LAYERS.draw_layer = MlxCanvas._mlx_new_layer(mlx_ptr)

    LAYERS.text_layer.contents.instances[0].z = 3
    LAYERS.draw_layer.contents.instances[0].z = 2
    LAYERS.grid_layer.contents.instances[0].z = 1

    MlxCanvas._fill_mlximg_by_color(LAYERS.grid_layer, 0xffffffff)

    GridMaker._create_graph_grid(LAYERS.grid_layer, LAYERS.text_layer, grid_config)

    return mlx_ptr


if __name__ == "__main__":
    grid_config: GridConfig = GridConfig._from_file("./config.toml")

    mlx_ptr = init_grid_window(grid_config)


    mlx.mlx_loop_hook(mlx_ptr, handel_input, ctypes.cast(mlx_ptr, c_void_p))
    mlx.mlx_mouse_hook(mlx_ptr, mouse_event, ctypes.cast(mlx_ptr, c_void_p))
    mlx.mlx_loop(mlx_ptr)
