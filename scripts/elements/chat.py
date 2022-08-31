import pygame
from scripts import common as c
from scripts.utility.scale_image import scale_image
from scripts.utility.size_element import size_element
from scripts.utility.font import renderText


def renderChat(element):
    data = c.data["el"][element]
    img = pygame.Surface(data[1], pygame.SRCALPHA)

    divider = size_element('assets/elements/chat/divider.png',(data[1][0]-50,5),(5,5,0,0))

    y = data[1][1]
    for row in reversed(data[3]):
        if row[0] == "EMPTY":
            y -= int(row[1]) * 30
            img.blit(divider, (0, y - 10))
            time_text = renderText(row[2], "custom", 15, font_type="small", col=(160, 160, 150))
            img.blit(time_text, (data[1][0] - 50, y - 28))

        else:
            y -= 110
            x = 0
            # Render icon
            if row[0] is not None:
                icon = c.image_store.get_image('projects/' + c.project_name + '/images/' + row[0] + '.png')
                icon = scale_image(icon,50)
                c.images_used.append(row[0] + '.png')
                img.blit(icon,(0,y+8))
                x = 45
            # Render text
            name_text = renderText(row[1],"custom", 25, font_type="small",col=(219,214,160))
            img.blit(name_text,(x,y))
            role_text = renderText(row[2], "custom", 17, font_type="small", col=(160, 160, 150))
            img.blit(role_text, (x, y+26))
            main_text = renderText(row[4], "custom", 25, font_type="small", col=(255, 255, 255))
            img.blit(main_text, (x, y + 50))

            img.blit(divider, (0, y - 10))
            time_text = renderText(row[3], "custom", 15, font_type="small", col=(160, 160, 150))
            img.blit(time_text, (data[1][0]-50, y - 28))

    return img
