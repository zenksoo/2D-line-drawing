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


        sx = x1 - x0
        sy = y1 - y0

        step = max(abs(sx), abs(sy))


        if (not step):
            return

        dx = sx / step
        dy = sy / step

        half = width // 2
        vx = -dy
        vy = dx


        print(vx, vy)

        x = x0
        y = y0
        MlxCanvas._draw_circle(layer, round(x + (vx * 10)), round(y + (10 * vy)), 5, pixel_color)
        for i in range(step):
            for j in range(-half, half):
                MlxCanvas._fill_pixel(layer, round(x + (vx * j)), round(y + (vy * j)), pixel_color)
            x += dx
            y += dy



