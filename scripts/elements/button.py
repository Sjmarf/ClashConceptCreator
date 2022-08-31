from scripts import common as c
import pygame
from scripts.utility import font
from scripts.utility.spritesheet import SpriteSheet
from scripts.utility.size_element import size_element
from scripts.utility.scale_image import scale_image


def renderButton(element):
    data = c.data["el"][element]

    if data[3] in {"more","drop-down"}:
        img = pygame.image.load('assets/elements/button/' + data[3] + '.png').convert_alpha()
    else:
        # img = size_element('assets/elements/button/' + data[3] + '.png', data[1], edge=(30, 30, 35, 20))
        if data[3] == "custom":
            img = c.image_store.get_tinted_image("button",data[7])
            img = size_element(img, data[1], edge=(30, 30, 35, 20), direct=True)
        else:
            try:
                img = size_element('assets/elements/button/'+data[3]+'.png', data[1], edge=(30, 30, 55, 20))
            except ValueError:
                img = size_element('assets/elements/button/' + data[3] + '.png', data[1], edge=(30, 30, 35, 20))

        if data[4] != "":
            text_surf = font.renderText(data[4], "default", int(data[5]))

        # Icon
        if data[6] is not None:
            icon = pygame.image.load('assets/elements/icon/' + data[6] + '.png').convert_alpha()
            icon = scale_image(icon,int(data[5])+10)
            if data[4] != "":
                text_surf2 = pygame.Surface((text_surf.get_width()+icon.get_width(),
                                             max(text_surf.get_height(),icon.get_height())),pygame.SRCALPHA)

                text_surf2.blit(icon,(0,text_surf2.get_height()//2-icon.get_height()//2))
                text_surf2.blit(text_surf,(icon.get_width(),text_surf2.get_height()//2-text_surf.get_height()//2))
                text_surf = text_surf2
            else:
                text_surf = icon

        if (data[6] is not None) or (data[4] != ""):
            img.blit(text_surf,
                     (img.get_width() // 2 - text_surf.get_width() // 2,
                      img.get_height() // 2 - text_surf.get_height() // 2))

    return img
