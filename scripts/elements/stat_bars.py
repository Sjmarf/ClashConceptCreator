import pygame

from scripts import common as c
from scripts.utility.size_element import size_element
from scripts.utility.scale_image import scale_image
from scripts.utility import font


def renderStatBars(element):
    data = c.data["el"][element]
    img = pygame.Surface(data[1], pygame.SRCALPHA)
    bar_width = data[1][0] - data[5] - 24
    bar_img = c.image_store.get_sized_image("stat bar","assets/elements/stat bars/bar1.png",
                                            (bar_width, data[5]), (30, 30, 17, 10))
    bar_img2 = c.image_store.get_tinted_image("stat_bars", data[4])
    bar_img2 = size_element(bar_img2, (bar_width, data[5]), (30, 30, 17, 10), direct=True)

    y = 20
    for row in data[3]:
        # Bar background
        img.blit(bar_img, (data[5]+24, y))
        # Bar foreground
        scale_factor = bar_width / int(row[3])
        width = int(row[2]) * scale_factor
        progress_surf = pygame.Surface((width, data[5]), pygame.SRCALPHA)
        progress_surf.blit(bar_img2, (0, 0))
        img.blit(progress_surf, (data[5]+24, y))
        # Text
        font_text = font.renderText(row[1], "default", 19)
        img.blit(font_text, (data[5]+29, y - 14))
        # Icon
        if row[0] is not None:
            icon = c.image_store.get_scaled_image('projects/'+c.project_name+'/images/'+row[0]+'.png',data[5]+19)
            img.blit(icon, (0, y - 9))
        y += data[5] + 20
    return img
