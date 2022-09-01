import pygame.image
from scripts import common as c
from scripts.utility.size_element import size_element
from scripts.utility.scale_image import scale_image
from scripts.utility.font import renderText


def renderGrid(element):
    data = c.data["el"][element]
    grid_type = data[8]
    img = size_element('assets/elements/grid/' + grid_type + '/background.png', data[1], (30, 30, 30, 50))

    if grid_type in {"skin", "donation"}:
        box_background = pygame.image.load('assets/elements/grid/' + grid_type + '/box_bg.png')
        grid_images = {0: c.image_store.get_image('assets/elements/grid/' + grid_type + '/box_0.png'),
                       1: c.image_store.get_image('assets/elements/grid/' + grid_type + '/box_1.png'),
                       2: c.image_store.get_image('assets/elements/grid/' + grid_type + '/box_2.png')}

    if grid_type == "magic item":
        grid_images = {0: pygame.transform.smoothscale(
            c.image_store.get_image('assets/elements/grid/' + grid_type + '/box_0.png'), (120, 85)),
            1: pygame.transform.smoothscale(
                c.image_store.get_image('assets/elements/grid/' + grid_type + '/box_1.png'), (120, 85)),
            2: pygame.transform.smoothscale(
                c.image_store.get_image('assets/elements/grid/' + grid_type + '/box_2.png'), (120, 85))}

    values = {"spacing_x": 145,
              "spacing_y": 145,
              "spacing_text": 50,
              "box_y_offset": 0,
              "box_width": 150,
              "icon_size_mult": 1,
              "font_size": 20,
              "font_y_offset": 0}

    if grid_type == "skin":
        values = {"spacing_x": 145,
                  "spacing_y": 145,
                  "spacing_text": 50,
                  "box_y_offset": 0,
                  "box_width": 150,
                  "icon_size_mult": 1,
                  "font_size": 20,
                  "font_y_offset": 25}

    elif grid_type == "donation":
        values = {"spacing_x": 80,
                  "spacing_y": 80,
                  "spacing_text": 50,
                  "box_y_offset": 0,
                  "box_width": 71,
                  "icon_size_mult": 1.4,
                  "font_size": 20,
                  "font_y_offset": 0}

    elif grid_type == "magic item":
        values = {"spacing_x": 145,
                  "spacing_y": 150,
                  "spacing_text": 60,
                  "box_y_offset": 50,
                  "box_width": 120,
                  "icon_size_mult": 1.4,
                  "font_size": 24,
                  "font_y_offset": 95}

    if len(data[3]) > 0:
        if data[7] == "centre":
            longest_line = len(max(data[3], key=len))
            start_x = data[1][0] // 2 - (longest_line * values["spacing_x"]) // 2
            if grid_type == "magic item":
                start_x += 10
            elif grid_type == "skin":
                start_x -= 3
        else:
            start_x = 10

        x, y = start_x, 10
        for line in data[3]:
            if not len(line) == 0:
                if type(line[0]) == str:
                    text_surf = renderText(line[0], "default", data[4])
                    img.blit(text_surf, (x + 10, y + 5 + values["spacing_text"] // 2 - text_surf.get_height() // 2))
                    y += values["spacing_text"]
                else:

                    for element in line:

                        # Draw box
                        if grid_type in {"skin", "donation"}:
                            img.blit(box_background, (x, y))
                        if grid_type == "magic item":
                            img.blit(grid_images[element[1]], (x, y + values["box_y_offset"]))

                        if element[0] is not None:
                            if element[1] == 2:
                                icon = c.image_store.get_monochrome_image(
                                    'projects/' + c.project_name + '/images/' + element[0] + '.png'
                                )
                            else:
                                icon = c.image_store.get_image(
                                    'projects/' + c.project_name + '/images/' + element[0] + '.png')
                            # Blit image
                            icon = scale_image(icon, data[5] * (values["box_width"] / 150) * values["icon_size_mult"])
                            offset = (values["box_width"] - data[5] * (values["box_width"] / 150) * values["icon_size_mult"]) // 2
                            img.blit(icon, (x + data[6][0] + offset, y + data[6][1] + offset))
                            c.images_used.append(element[0] + ".png")

                        # Draw outer frame
                        if grid_type in {"skin", "donation"}:
                            img.blit(grid_images[element[1]], (x, y))
                        # Blit text
                        text_surf = renderText(element[2], "default", values["font_size"])
                        img.blit(text_surf,
                                 (x + values["box_width"] // 2 - text_surf.get_width() // 2,
                                  y + values["font_y_offset"]))

                        x += values["spacing_x"]
                    y += values["spacing_y"]
                x = start_x

    return img
