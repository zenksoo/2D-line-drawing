from MLX.libmlx import *
from MLXCanvas import MlxCanvas

import math

class LineDrawing:
    def __new__(cls) -> Self:
        raise ValueError(
            "you can't create Object from LineDrawing Class")


    @staticmethod
    def drawLine(layer: mlx_image_t,
                 x0: int, y0: int, x1: int, y1: int,
                 width: int, pixel_color: int) -> None:
        dx = x1 - x0
        dy = y1 - y0

        step = max(dx, dy)

        half = width // 2

        length = math.sqrt(dx*dx + dy*dy)
        nx = -dy / length
        ny = dx / length

        # (nx, ny) is the unit of 90deg of the line D

        if (step):
            stepx = dx / step
            stepy = dy / step
            for i in range(step + 1):
                px = math.ceil(x0 + i * stepx)
                py = math.ceil(y0 + i * stepy)
                for j in range(-half, half + 1):
                    ox = round(px + j * nx)
                    oy = round(py + j * ny)

                    MlxCanvas._fill_pixel(layer, ox, oy, pixel_color)
