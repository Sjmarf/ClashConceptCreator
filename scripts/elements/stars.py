from scripts import common as c
import pygame
from scripts.utility.scale_image import scale_image
from scripts.utility.font import renderText

def renderStars(element):
    data = c.data["el"][element]
    star_size = data[1][1]

    img = pygame.Surface(data[1], pygame.SRCALPHA)
    star1 = c.image_store.get_image("assets/elements/stars/1a.png")
    star1 = scale_image(star1,star_size)
    star2 = c.image_store.get_image("assets/elements/stars/1b.png")
    star2 = scale_image(star2,star_size)

    if data[4] != "":
        positions = [0,star_size*1.2,star_size*2.4]
        text_surf = renderText(data[4],"default",int(star_size*0.8))
        img.blit(text_surf,(data[1][0]-text_surf.get_width(),data[1][1]-text_surf.get_height()*0.9))
    else:
        positions = [data[1][0]//2-star_size*1.7,data[1][0]//2-star_size//2,data[1][0]//2+star_size*0.7]

    for num, x_pos in enumerate(positions):
        if int(data[3]) > num:
            img.blit(star2, (x_pos,0))
        else:
            img.blit(star1, (x_pos, 0))

    return img
