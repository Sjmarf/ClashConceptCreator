from pygame import Color, PixelArray
from time import time

def tint_image(surf,col,original_col):
    pixels = PixelArray(surf)

    # Convert colour to HSVA
    col_obj = Color(col)
    offset = tuple(col_obj.hsva)
    start_time = time()

    for x in range(surf.get_width()):
        for y in range(surf.get_height()):
            # Turn the pixel data into an RGB tuple
            rgb = surf.unmap_rgb(pixels[x][y])
            # Get a new color object using the RGB tuple and convert to HSLA
            color = Color(*rgb)
            h, s, l, a = color.hsla
            # Add value to the hue and wrap to under 360
            color.hsla = ((int(h) + offset[0] - original_col[0]) % 360,
                          min(100, max(0, int(s) - original_col[1] + offset[1])),
                          min(100, max(0, int(l) - original_col[2] + offset[2])),
                          min(100, max(0, int(a))))
            # Assign directly to the pixel
            pixels[x][y] = color

    del pixels
    print("Image tint took "+str(round(time() - start_time, 3))+"s")
    return surf
