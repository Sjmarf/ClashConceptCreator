from scripts import common as c
from scripts.utility.font import renderText
from scripts.utility.scale_image import scale_image
from pygame import Surface, SRCALPHA, font
import re


def renderTextBlock(element):
    data = c.data["el"][element]
    new_surf = Surface(data[1],SRCALPHA)
    text = data[3].split("\n")

    font_name = data[7].replace("2","")
    temp_font = font.Font('assets/fonts/'+font_name+'.ttf', data[4])

    if font_name == "small":
        gap_size = " "*int(5*data[8]/100)
    else:
        gap_size = " "*int(4*data[8]/100)

    y = 10
    for emoji_list,line in zip(data[10],text):
        line2 = line.replace(" ", gap_size)
        if "2" not in data[7]:
            text_surf = renderText(line2,"custom",data[4],font_type=font_name,col=data[6])
        else:
            text_surf = renderText(line2, "custom", data[4], font_type=font_name, col=data[6],
                                   border=max(1, data[4] / 25), thickness=max(3,data[4] // 6.25))
        if data[5] == "centre":
            start_x = data[1][0]//2-text_surf.get_width()//2
        elif data[5] == "left":
            start_x = 0
        else:
            start_x = data[1][0]-text_surf.get_width()

        new_surf.blit(text_surf, (start_x, y))

        for emoji in emoji_list:
            space_count = line[:emoji[1]].count(" ")
            line3 = line.replace(" ", " ")
            x = 8+temp_font.size(line3[:emoji[1]]+space_count*gap_size[:-1])[0]

            img = c.image_store.get_scaled_image(
                "projects/" + c.project_name + "/images/" + emoji[0] + ".png", data[4]*data[8]/100)
            if img is not None:
                new_surf.blit(img, (start_x+x, y+data[4]//2-((data[4]-2)*data[8]/100)//2+5))

        y += (data[4]+5)*data[9]/100

    return new_surf
