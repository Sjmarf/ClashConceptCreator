from scripts import common as c
from scripts.utility.size_element import size_element
from scripts.utility.scale_image import scale_image
from scripts.utility.font import renderText
import pygame


def renderTabs(element):
    data = c.data["el"][element]
    img = pygame.Surface(data[1],pygame.SRCALPHA)
    tab_img1 = pygame.image.load('assets/elements/tab/tab'+data[5]+'a.png').convert_alpha()
    tab_img2 = pygame.image.load('assets/elements/tab/tab'+data[5]+'b.png').convert_alpha()
    number_of_tabs,width = len(data[3]), data[1][0]
    spacing = width//number_of_tabs
    half = tab_img1.get_width()//2
    offset = spacing//2 - half

    for tab in range(number_of_tabs):
        x = spacing * tab + offset
        if tab == data[4]:
            img.blit(tab_img1,(x, 0))
        else:
            img.blit(tab_img2, (x, 0))
        if data[5] == "2":
            if data[3][tab] is not None and data[3][tab] != "":
                try:
                    icon = pygame.image.load('assets/elements/icon/'+data[3][tab]+'.png').convert_alpha()
                    icon = scale_image(icon,40)
                    img.blit(icon, (x + half - icon.get_width()//2, 20))
                except FileNotFoundError:
                    pass

        else:
            text_surf = renderText(data[3][tab], "default", 22)
            img.blit(text_surf,(x+half-text_surf.get_width()//2, 20))

    return img
