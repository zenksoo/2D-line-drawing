from MLX.libmlx import *
from MLXCanvas import MlxCanvas

import math

class LineDrawing:
    def __new__(cls) -> Self:
        raise ValueError(
            "you can't create Object from LineDrawing Class")

    @staticmethod
    def _draw_line(layer: mlx_image_t,
                                 x0: int, y0: int, x1: int, y1: int,
                                 thickness: int, pixel_color: int) -> None:

        sx = x1 - x0
        sy = y1 - y0

        step = max(abs(sx), abs(sy))

        if not step: return

        dx = sx / step
        dy = sy / step

        half = thickness // 2
        vx = -dy
        vy = dx

        for i in range(-half, half + 1):
            x = round(x0 + (vx * i))
            y = round(y0 + (vy * i))
            if (thickness > 1):
                r = 1
            else:
                r = 0

            for i in range(step):
                MlxCanvas._draw_circle(layer, round(x), round(y), r, pixel_color)
                x += dx
                y += dy
