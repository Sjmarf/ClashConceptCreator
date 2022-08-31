import pygame

from scripts import common as c
from scripts.utility.size_element import size_element
from pygame import image,Surface,SRCALPHA
from scripts.utility import font


def renderStatList(element):
    data = c.data["el"][element]
    img = pygame.Surface(data[1],pygame.SRCALPHA)
    y = 0
    divider = pygame.image.load('assets/elements/stat list/divider.png').convert()
    divider = pygame.transform.scale(divider,(data[1][0],4))

    for line in data[3]:
        text_surf = font.renderText(line[0],'custom',data[8],font_type=data[6],col=data[4])
        img.blit(text_surf,(0,y))
        text_surf = font.renderText(line[1], 'custom', data[9], font_type=data[7], col=data[5])
        img.blit(text_surf, (data[1][0]-text_surf.get_width(), y))
        img.blit(divider,(0,y+max(data[8],data[9])+10))
        y += max(data[8],data[9])+17
    return img
