import pygame
from scripts.utility.size_element import size_element
from scripts.utility.scale_image import scale_image
from scripts.utility.font import renderText
from scripts import common as c


def renderList(element):
    data = c.data["el"][element]
    img = pygame.Surface(data[1], pygame.SRCALPHA)
    row_img = size_element('assets/elements/list/row1.png', (data[1][0], 85), (30, 30, 30, 30))
    divider_img = pygame.image.load('assets/elements/list/divider.png').convert_alpha()
    counter_img = pygame.image.load('assets/elements/list/counter.png').convert_alpha()
    mult = data[1][0] / 100
    y = 0
    for row in data[4]:
        img.blit(row_img, (0, y))
        x = 0
        for (part, item) in zip(data[3], row):
            centre = x * mult + (part[1] * mult // 2)
            if part[0] == "text":
                text_surf = renderText(item[0], "default", 22)
                img.blit(text_surf, (x * mult + 10, y + 20))

            elif part[0] == "double text":
                text_surf = renderText(item[0], "default", 22)
                img.blit(text_surf, (x * mult + 5, y + 7))
                text_surf = renderText(item[1], "small2", 16)
                img.blit(text_surf, (x * mult + 5, y + 35))

            elif part[0] == "image":
                if item[0] is not None:
                    c.images_used.append(item[0] + ".png")
                    part_img = pygame.image.load(
                        'projects/' + c.project_name + '/images/' + item[0] + ".png").convert_alpha()
                    size = data[6]//2
                    part_img = scale_image(part_img, size)
                    img.blit(part_img, ((x * mult) + (part[1] * mult // 2) - size//2, y+((85-size)//2)))

            elif part[0] == "counter":
                img.blit(counter_img, (centre - 52, y))
                text_surf = renderText(item[0], "small2", 16)
                img.blit(text_surf, (centre - text_surf.get_width()//2, y + 6))
                text_surf = renderText(item[1], "custom", 19, font_type="small",col=(40,40,40))
                img.blit(text_surf, (centre - text_surf.get_width() // 2, y + 33))

            elif part[0] == "readout":
                readout_img = pygame.image.load('assets/elements/list/readout.png').convert_alpha()
                img.blit(readout_img, (centre - readout_img.get_width() // 2, y))
                text_surf = renderText(item[0], "default", 22)
                img.blit(text_surf, (centre - readout_img.get_width() // 2 + 5, y + 23))

            x += part[1]
            if x < 100 and part[2]:
                img.blit(divider_img, (x * mult, y))
        y += 95

    return img
