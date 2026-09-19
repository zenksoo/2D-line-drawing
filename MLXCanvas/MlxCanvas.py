from MLX.libmlx import *
from typing import Dict, Tuple
from PIL import Image
from Utils import pack_rgba

class MlxCanvas:
    @staticmethod
    def _fill_pixel(img: mlx_image_t,
                x: int, y: int,
                pixel_color: int) -> None:

        idx = (y * img.contents.width + x) * 4
        img.contents.pixels[idx] = pixel_color >> 24 & 0xFF
        img.contents.pixels[idx + 1] = pixel_color >> 16 & 0xFF
        img.contents.pixels[idx + 2] = pixel_color >> 8 & 0xFF
        img.contents.pixels[idx + 3] = pixel_color & 0xFF

    @staticmethod
    def _mlx_new_layer(mlx_ptr: mlx_t) -> mlx_image_t:
        w, h = (mlx_ptr.contents.width, mlx_ptr.contents.height)

        layer: mlx_image_t = mlx.mlx_new_image(mlx_ptr, w, h)

        mlx.mlx_image_to_window(mlx_ptr, layer, 0, 0)

        return layer

    @staticmethod
    def _fill_mlximg_by_color(img: mlx_image_t, pixel_color: int) -> None:
        for y in range(img.contents.height):
            for x in range(img.contents.width):
                MlxCanvas._fill_pixel(img, x, y, pixel_color)

    @staticmethod
    def _erase_mlximg(mlx_ptr: mlx_t, img: mlx_image_t) -> mlx_image_t:
        w, h = (img.contents.width, img.contents.height)
        x, y = (
            img.contents.instances[0].x,
            img.contents.instances[0].y
        )


        mlx.mlx_delete_image(mlx_ptr, img)

        img = mlx.mlx_new_image(mlx_ptr, w, h)
        mlx.mlx_image_to_window(mlx_ptr, img, x, y)

        return img

    @staticmethod
    def _draw_text(layer: mlx_image_t,
                txt: str, txt_x: int, txt_y: int,
                color: int | None = None
                ) -> Dict[str, Tuple[int, int]]:

        def draw_char(img: mlx_image_t,
                        char: str, char_idx: int,
                        layer_x: int, layer_y: int,
                        replacement_color: int | None) -> None:
            LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
            UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            DIGITS = "1234567890!\"#%'()~+-/[]<>:.,_| "

            png: Image.Image
            glyph_x: int = 0
            if char in LOWERCASE:
                png = Image.open("./Assets/fonts/lowercase.png")
                glyph_x = LOWERCASE.index(char)
            elif char in UPPERCASE:
                png = Image.open("./Assets/fonts/uppercase.png")
                glyph_x = UPPERCASE.index(char)
            elif char in DIGITS:
                png = Image.open("./Assets/fonts/digits.png")
                glyph_x = DIGITS.index(char)
            else:
                char = '.'
                png = Image.open("./Assets/fonts/digits.png")
                glyph_x = DIGITS.index(char)

            glyph_x = glyph_x * 6
            img_x = char_idx * 6

            for y in range(8):
                for x in range(6):
                    pixel_color = pack_rgba(*png.getpixel((glyph_x + x, y)))
                    if (replacement_color and
                        pixel_color == (0xffffff << 8) + 0xff):

                        pixel_color = replacement_color

                    MlxCanvas._fill_pixel(img, img_x + x + layer_x,
                                        y + layer_y, pixel_color)

        for idx, char in enumerate(txt):
            draw_char(layer, char, idx, txt_x, txt_y, color)

        return {
            "start": (txt_x, txt_y),
            "end": (txt_x + (len(txt) * 6), txt_y + 8)
        }

    @staticmethod
    def _draw_circle(layer: mlx_image_t, cx: int, cy: int, r: int, pixel_color: int) -> None:
        x = 0
        y = -r

        while (x < -y):
            midp = y + 0.5
            c = midp*midp + x*x

            if c > r*r:
                y += 1

            MlxCanvas._fill_pixel(layer, cx + x, cy + y, 0x000000ff)
            MlxCanvas._fill_pixel(layer, cx + x, cy - y, 0x000000ff)
            MlxCanvas._fill_pixel(layer, cx - x, cy + y, 0x000000ff)
            MlxCanvas._fill_pixel(layer, cx - x, cy - y, 0x000000ff)

            MlxCanvas._fill_pixel(layer, cx + y, cy + x, 0x000000ff)
            MlxCanvas._fill_pixel(layer, cx - y, cy - x, 0x000000ff)
            MlxCanvas._fill_pixel(layer, cx - y, cy + x, 0x000000ff)
            MlxCanvas._fill_pixel(layer, cx + y, cy - x, 0x000000ff)


            for i in range(cx - x, cx + x + 1):
                MlxCanvas._fill_pixel(layer, i, cy + y, pixel_color)
                MlxCanvas._fill_pixel(layer, i, cy - y, pixel_color)

            for i in range(cx + y, cx - y):
                MlxCanvas._fill_pixel(layer, i, cy + x, pixel_color)
                MlxCanvas._fill_pixel(layer, i, cy - x, pixel_color)

            x += 1
