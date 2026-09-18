from MLX.libmlx import *
from MLXCanvas import MlxCanvas
from GridConfig import GridConfig
from GridMaker import GridMaker
from LineDrawing import LineDrawing

from enum import Enum
from PIL import Image
from typing import Dict, Tuple
import os


import ctypes

# will be start | end | none
# if none mean start and end points are selected and the line is drawed
# you meed to click on left mouse button to reset and clean the drawing layer

class Coordinate:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

class DrawState(Enum):
    START_POINT = 1
    END_POINT = 2
    LINE_DRAWING = 3
    ERASE = 4

# drawing state
# start point -> end point -> line -> erase window


draw_state: DrawState = DrawState.START_POINT
start_point: Coordinate = Coordinate(0, 0)
end_point: Coordinate = Coordinate(0, 0)


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

    # x = ctypes.c_uint32(0)
    # y = ctypes.c_uint32(0)


    # mlx.mlx_get_mouse_pos(mlx_ptr, ctypes.byref(x), ctypes.byref(y))

    # if (x.value <= mlx_ptr.contents.width and x.value >= 0 and
    #     y.value <= mlx_ptr.contents.height and y.value >= 0):
    #     MlxCanvas._draw_circle(layers.draw_layer, x.value, y.value, 10, 0xff0000ff)

@mlx_mousefunc
def mouse_event(button, x, y, param) -> None:
    mlx_ptr = ctypes.cast(param, ctypes.POINTER(mlx_t))
    x = ctypes.c_uint32(0)
    y = ctypes.c_uint32(0)

    mlx.mlx_get_mouse_pos(mlx_ptr, ctypes.byref(x), ctypes.byref(y))
    global draw_state

    if (button == 0):
        if draw_state != DrawState.ERASE:
            MlxCanvas._draw_circle(layers.draw_layer, x.value, y.value, 10, 0x139AB9FF)
            if (draw_state == DrawState.START_POINT and
                (x.value != end_point.x and y.value != end_point.y)):
                start_point.x = x.value
                start_point.y = y.value
                draw_state = DrawState.END_POINT
            elif (draw_state == DrawState.END_POINT and
                  (x.value != start_point.x and y.value != start_point.y)):
                end_point.x = x.value
                end_point.y = y.value
                draw_state = DrawState.LINE_DRAWING
                # drawing line here
                LineDrawing.drawLine(layers.draw_layer,
                                     start_point.x, start_point.y,
                                     end_point.x, end_point.y, 20,
                                     0xDE06C1FF)
                draw_state = DrawState.START_POINT

    elif (button == 1):
        MlxCanvas._erase_mlximg(layers.draw_layer)



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
    mlx.mlx_mouse_hook(mlx_ptr, mouse_event, ctypes.cast(mlx_ptr, c_void_p))
    mlx.mlx_loop(mlx_ptr)
    pass
