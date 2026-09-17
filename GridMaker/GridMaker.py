from MLX.libmlx import *
from MLXCanvas import MlxCanvas


class GridMaker:
    def __new__(cls, *args, **kwargs) -> Self:
        raise ValueError(
            "you can't create Object From this Class"
        )

    @staticmethod
    def _draw_axis(img: mlx_image_t,
                   x0: int, y0: int,
                   x1: int, y1: int,
                   line_width: int) -> None:

        for y in range(y0 - line_width, y0 + 1):
            for x in range(x0 - line_width, x1 + 1):
                MlxCanvas._fill_pixel(img, x, y, line_width)

        for x in range(x0 - line_width, x0):
            for y in range(y0 - line_width, y1 + 1):
                MlxCanvas._fill_pixel(img, x, y, line_width)

    @staticmethod
    def _draw_labels(text_layer: mlx_image_t,
                     x0: int, y0: int,
                     x1: int, y1: int,
                     line_width: int,
                     grid_size: int) -> None:

        x_label: int = 0
        y_label: int = 0

        for x in range(x0 - line_width, x1 + 1, grid_size):
            if (x == x0 - line_width):
                MlxCanvas._draw_text(text_layer, "0", x - 15, y0 - line_width - 15, 0x000000ff)
            else:
                MlxCanvas._draw_text(text_layer, str(x_label), x, y0 - 20, 0x000000ff)
            x_label += 1

        for y in range(y0 - line_width, y1 + 1, grid_size):
            if (y == y0 - line_width):
                MlxCanvas._draw_text(text_layer, "0", x0 - line_width - 15, y - 15, 0x000000ff)
            else:
                MlxCanvas._draw_text(text_layer, str(y_label), x0 - 20, y, 0x000000ff)
            y_label += 1

    @staticmethod
    def _create_graph_grid(grid_layer, text_layer, x0, y0, x1, y1, pixel_color, grid_size) -> None:
        # randomize grid area
        start_y = y0 + grid_size
        end_y = y1 - grid_size
        start_x = x0 + grid_size
        end_x = x1 - grid_size

        GridMaker._draw_axis(grid_layer, start_x, start_y, end_x, end_y, 3)
        GridMaker._draw_labels(text_layer, start_x, start_y, end_x, end_y, 3, grid_size)

        for y in range(start_y, end_y + 1, grid_size):
            for x in range(start_x, end_x):
                MlxCanvas._fill_pixel(grid_layer, x, y, pixel_color)
            y += grid_size

        for x in range(start_x, end_x + 1, grid_size):
            for y in range(start_y, end_y):
                MlxCanvas._fill_pixel(grid_layer, x, y, pixel_color)
            x += grid_size

