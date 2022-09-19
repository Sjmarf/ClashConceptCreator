from scripts import common as c
from scripts.utility.font import renderText
from pygame import Surface, SRCALPHA


def renderTroop(element):
    data = c.data["el"][element]
    new_surf = Surface(data[1], SRCALPHA)
    box = c.image_store.get_sized_image('troop_box', 'assets/elements/troop/box.png', (55, 78), (10, 10, 10, 10))
    level_box = c.image_store.get_sized_image('troop_level', 'assets/elements/troop/level.png', (30, 30),
                                              (10, 10, 10, 10))
    x = 0
    for item in data[3]:
        this_box = box.copy()
        if item[0] is not None:
            icon = c.image_store.get_scaled_image('projects/' + c.project_name + '/images/' + item[0] + '.png', 53)
            this_box.blit(icon, (1, this_box.get_height() - 52))

        if item[1] != "":
            text_surf = renderText(item[1], "custom", size=18, font_type='large', col=(238, 128, 125),
                                   border=max(1, 18 // 25), thickness=max(3, 18 // 6.25))
            this_box.blit(text_surf, (2, 2))

        if item[2] != "":
            this_box.blit(level_box, (0, this_box.get_height() - 30))
            text_surf = renderText(item[2], 'custom', 15, font_type='small', col=(255, 255, 255))
            this_box.blit(text_surf, (14 - text_surf.get_width() // 2, this_box.get_height() - 29))

        new_surf.blit(this_box, (x, 0))
        x += 60
    return new_surf
