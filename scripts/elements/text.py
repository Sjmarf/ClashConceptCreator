from scripts import common as c
from scripts.utility.font import renderText
from pygame import Surface, SRCALPHA


def renderTextEl(element):
    data = c.data["el"][element]
    new_surf = Surface(data[1],SRCALPHA)
    if "2" in data[7]:
        name = data[7][:-1]
        text_surf = renderText(data[3],"custom",size=data[4],font_type=name,col=data[6],
                               border=max(1,data[4]/25), thickness=max(3,data[4]//6.25))
    else:
        text_surf = renderText(data[3], "custom", size=data[4], font_type=data[7], col=data[6])
    if data[5] == "centre":
        pos = (data[1][0] // 2 - text_surf.get_width() // 2)
    elif data[5] == "left":
        pos = 0
    else:
        pos = data[1][0]-text_surf.get_width()
    new_surf.blit(text_surf,(pos,data[1][1] // 2 - text_surf.get_height() // 2))

    return new_surf
