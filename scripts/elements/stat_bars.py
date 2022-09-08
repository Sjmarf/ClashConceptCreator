import pygame

from scripts import common as c
from scripts.utility.size_element import size_element
from scripts.utility.scale_image import scale_image
from scripts.utility import font


def renderBars(element):
    data = c.data["el"][element]
    img = pygame.Surface(data[1], pygame.SRCALPHA)

    if data[6] == "stat":
        prefs = {"bar_width": data[1][0] - data[5] - 24,
                 "bar_start_x": data[5]+24,
                 "text_x": data[5] + 29,
                 "text_y": -14,
                 "icon_size": data[5]+19,
                 "icon_pos": [0, - 9],
                 "line_spacing": data[5] + 20,
                 "foreground_first": False
                 }

    else:
        prefs = {"bar_width": data[1][0],
                 "bar_start_x": 0,
                 "text_x": data[5]+29,
                 "text_y": data[5]//2-15,
                 "icon_size": data[5] + 23,
                 "icon_pos": [8, - 11],
                 "line_spacing": data[5] + 36,
                 "foreground_first": True
                 }

    if data[7] == "right":
        prefs["icon_pos"][0] = data[1][0] - prefs["icon_pos"][0] - prefs["icon_size"]
        prefs["bar_end_x"] = prefs["bar_start_x"]
        prefs["bar_start_x"] = 0

    bar_img = c.image_store.get_sized_image("bar","assets/elements/stat bars/"+data[6]+"/bar1.png",
                                            (prefs["bar_width"], data[5]), (30, 30, 17, 10))
    if data[6] == "stat":
        bar_img2 = c.image_store.get_tinted_image("stat_bars", data[4])
        bar_img2 = size_element(bar_img2, (prefs["bar_width"], data[5]), (30, 30, 17, 10), direct=True)
    else:
        if data[7] == "right":
            bar_img2 = c.image_store.get_image("assets/elements/stat bars/resource/bar2-right.png")
            bar_img2 = size_element(bar_img2, (prefs["bar_width"], data[5]), (0, 10, 10, 10), direct=True)
        else:
            bar_img2 = c.image_store.get_image("assets/elements/stat bars/resource/bar2-left.png")
            bar_img2 = size_element(bar_img2, (prefs["bar_width"], data[5]), (10, 0, 10, 10), direct=True)
        bar_img2.fill(data[4],special_flags=pygame.BLEND_RGB_ADD)

    y = 20
    for row in data[3]:
        # Bar background
        if not prefs["foreground_first"]:
            img.blit(bar_img, (prefs["bar_start_x"], y))
        # Bar foreground
        scale_factor = prefs["bar_width"] / int(row[3])
        width = int(row[2]) * scale_factor
        progress_surf = pygame.Surface((width, data[5]), pygame.SRCALPHA)
        if data[7] == "right":
            progress_surf.blit(bar_img2, (width-bar_img2.get_width(), 0))
            img.blit(progress_surf, (data[1][0] - width - prefs["bar_end_x"], y))
        else:
            progress_surf.blit(bar_img2, (0, 0))
            img.blit(progress_surf, (prefs["bar_start_x"], y))
        # Background
        if prefs["foreground_first"]:
            img.blit(bar_img, (prefs["bar_start_x"], y))
        # Text
        font_text = font.renderText(row[1], "default", 19)
        if data[7] == "right":
            img.blit(font_text, (data[1][0] - prefs["text_x"] - font_text.get_width(), y + prefs["text_y"]))
        else:
            img.blit(font_text, (prefs["text_x"], y + prefs["text_y"]))
        # Icon
        if row[0] is not None:
            icon = c.image_store.get_scaled_image('projects/'+c.project_name+'/images/'+row[0]+'.png',prefs["icon_size"])
            img.blit(icon, (prefs["icon_pos"][0],y+prefs["icon_pos"][1]))
        y += prefs["line_spacing"]
    return img
