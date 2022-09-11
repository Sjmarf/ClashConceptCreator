import pygame

from scripts import common as c
from scripts.utility.size_element import size_element
from pygame import image,Surface,SRCALPHA


def renderBox(element):
    data = c.data["el"][element]
    if data[3] == "map":
        temp_surf = Surface(data[1],SRCALPHA)
        temp_surf.fill((126,127,101))
        bg = c.image_store.get_image('assets/elements/box/map_bg.png')
        temp_surf.blit(bg,(data[1][0]//2-466,data[1][1]//2-147))
        cutout = size_element('assets/elements/box/cutout.png', data[1], (30, 30, 30, 30))
        temp_surf.blit(cutout,(0,0))
        img = Surface(data[1], SRCALPHA)
        temp_surf.set_colorkey((255,0,255))
        img.blit(temp_surf,(0,0))
        box = c.image_store.get_sized_image('box_map','assets/elements/box/map.png', data[1], (30, 30, 30, 30))
        img.blit(box,(0,0))

    elif data[3] == "gradient":
        gradient_surf = pygame.Surface((1,3),pygame.SRCALPHA)
        gradient_surf.set_at((0,0),data[4])
        col = list(data[4])
        if len(col) < 4:
            col.append(50)
        else:
            col[3] = 50
        gradient_surf.set_at((0, 1), col)
        img = pygame.transform.smoothscale(gradient_surf,data[1])
        cutout = size_element('assets/elements/box/cutout2.png', data[1], (30, 30, 30, 30))
        img.blit(cutout,(0,0),special_flags=pygame.BLEND_RGBA_SUB)

    elif data[3] == "highlight":
        img = size_element('assets/elements/box/custom1.png', data[1], (30, 30, 30, 30))
        img.fill(data[4], special_flags=pygame.BLEND_RGB_ADD)
        img2 = size_element('assets/elements/box/custom1.png', (data[1][0]-20,data[1][1]//2-10), (30, 30, 30, 30))
        col = (data[4][0]+20,data[4][1]+20,data[4][2]+20)
        img2.fill(col, special_flags=pygame.BLEND_RGB_ADD)
        img.blit(img2,(10,10))

    else:
        img = c.image_store.get_sized_image('box_solid1','assets/elements/box/custom1.png', data[1], (20, 20, 20, 20))
        img.fill(data[4],special_flags=pygame.BLEND_RGB_ADD)
        outline = c.image_store.get_sized_image('box_solid_2','assets/elements/box/custom2.png', data[1], (20, 20, 20, 20))
        # 100, 150, 120
        col = (max(0,200-data[4][0]),max(0,200-data[4][1]),max(0,200-data[4][2]))
        outline.fill(col, special_flags=pygame.BLEND_RGB_SUB)
        img.blit(outline,(0,0))

    opacity = 255-(data[5]/100*255)
    img.fill((0,0,0,opacity),special_flags=pygame.BLEND_RGBA_SUB)
    return img
