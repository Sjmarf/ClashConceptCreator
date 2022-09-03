from scripts import common as c
import pygame
from scripts.utility import font
from scripts.utility.scale_image import scale_image


def renderPlayerInfo(element):
    data = c.data["el"][element]
    img = pygame.Surface(data[1], pygame.SRCALPHA)

    name_y, clan_y = data[1][1] * 0.2, data[1][1] * 0.5

    # Icon
    if data[3] is not None:
        icon = c.image_store.get_image("projects/" + c.project_name + "/images/" + data[3] + ".png")
        icon = scale_image(icon, data[1][1] * 0.9)
    # Header
    if data[6] != "":
        size = int(data[1][1] * 0.25)
        header_surf = font.renderText(data[6], "custom", size, font_type="small", col=(254, 253, 165),
                                      border=max(1, size / 25), thickness=max(3, size // 6.25))
        name_y, clan_y = name_y + data[1][1] * 0.15, clan_y + data[1][1] * 0.15
    # Name
    name_surf = font.renderText(data[4], "default", int(data[1][1] * 0.3))
    # Clan
    clan_surf = font.renderText(data[5], "default", int(data[1][1] * 0.25))

    if data[7] == "left":
        name_x, clan_x, header_x = data[1][1], data[1][1], data[1][1]
        # Blit icon
        if data[3] is not None:
            img.blit(icon, (0, data[1][1] * 0.05))
    else:
        name_x, clan_x = data[1][0]-data[1][1]-name_surf.get_width(),\
                                   data[1][0]-data[1][1]-clan_surf.get_width()
        if data[6] != "":
            header_x = data[1][0] - data[1][1] - header_surf.get_width()
        # Blit icon
        if data[3] is not None:
            img.blit(icon, (data[1][0]-data[1][1], data[1][1] * 0.05))

    # Blit text
    img.blit(name_surf, (name_x, name_y))
    img.blit(clan_surf, (clan_x, clan_y))
    if data[6] != "":
        img.blit(header_surf, (header_x, 0))

    return img
