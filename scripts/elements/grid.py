import pygame.image
from scripts import common as c
from scripts.utility.size_element import size_element
from scripts.utility.scale_image import scale_image
from scripts.utility.font import renderText


def renderGrid(element):
    data = c.data["el"][element]
    grid_type = data[8]
    img = size_element('assets/elements/grid/'+grid_type+'/background.png', data[1], (30,30,30,50))

    box_background = pygame.image.load('assets/elements/grid/'+grid_type+'/box_bg.png')
    grid_images = {0: pygame.image.load('assets/elements/grid/'+grid_type+'/box_0.png').convert_alpha(),
                   1: pygame.image.load('assets/elements/grid/'+grid_type+'/box_1.png').convert_alpha(),
                   2: pygame.image.load('assets/elements/grid/'+grid_type+'/box_2.png').convert_alpha()}

    # Calculate the position of grid
    spacing_x, spacing_y, spacing_text, box_width, icon_size_mult = 145, 145, 50, 150, 1

    if grid_type == "skin":
        spacing_x, spacing_y, spacing_text, box_width, icon_size_mult = 145, 145, 50, 150, 1
    elif grid_type == "donation":
        spacing_x, spacing_y, spacing_text, box_width, icon_size_mult = 80, 80, 50, 71, 1.4

    if len(data[3]) > 0:
        if data[7] == "centre":
            longest_line = len(max(data[3], key=len))
            start_x = data[1][0] // 2 - (longest_line * spacing_x) // 2 - 3
        else:
            start_x = 10

        x, y = start_x, 10
        for line in data[3]:
            if not len(line) == 0:
                if type(line[0]) == str:
                    text_surf = renderText(line[0], "default", data[4])
                    img.blit(text_surf, (x + 10, y + 5 + spacing_text // 2 - text_surf.get_height() // 2))
                    y += spacing_text
                else:

                    for element in line:
                        img.blit(box_background, (x, y))
                        if element[0] is not None:
                            # Blit image
                            icon = pygame.image.load('projects/' + c.project_name + '/images/' + element[0] + '.png')
                            icon = scale_image(icon, data[5]*(box_width/150)*icon_size_mult)
                            offset = (box_width - data[5]*(box_width/150)*icon_size_mult) // 2
                            img.blit(icon, (x + data[6][0] + offset, y + data[6][1] + offset))
                            c.images_used.append(element[0] + ".png")

                        img.blit(grid_images[element[1]], (x, y))
                        x += spacing_x
                    y += spacing_y
                x = start_x

    return img
