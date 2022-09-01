from scripts import common as c
import pygame
from scripts.utility import font
from scripts.utility.size_element import size_element


def renderMenu(element):
    data = c.data["el"][element]
    text_surf = font.renderText(data[4], "default", int(data[5]))
    new_width, new_height = data[1]
    if new_width < 200:
        c.data["el"][element][1] = (200, new_height)
        new_width = 200
    if new_height < 200:
        c.data["el"][element][1] = (new_width, 200)
        new_height = 200

    img = c.image_store.get_sized_image("menu "+data[3],'assets/foregrounds/' + data[3] + '.png',(new_width, new_height))
    if data[3] == "menu_4":
        title_y = 42
    else:
        title_y = 50
    img.blit(text_surf,
             (img.get_width() // 2 - text_surf.get_width() // 2, title_y - text_surf.get_height() // 2))

    return img
