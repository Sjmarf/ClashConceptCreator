from scripts import common as c
from scripts.utility.font import renderText
from scripts.utility.scale_image import scale_image
from pygame import Surface, SRCALPHA, font
import re


def renderTextBlock(element):
    EMOJI_PATTERN = re.compile(
        "(["
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "])"
    )

    data = c.data["el"][element]
    new_surf = Surface(data[1],SRCALPHA)
    text = data[3].split("\n")

    temp_font = font.Font('assets/fonts/'+data[7]+'.ttf', data[4])

    if data[7] == "small":
        gap_size = "      "
    else:
        gap_size = "    "
    y = 0
    for line in text:
        parts = re.split(EMOJI_PATTERN, line)
        line2 = re.sub(EMOJI_PATTERN, gap_size, line)
        if data[7] == "small":
            text_surf = renderText(line2,"custom",data[4],font_type="small",col=data[6])
        else:
            text_surf = renderText(line2, "custom", data[4], font_type="large", col=data[6],
                                   border=max(1, data[4] / 25), thickness=data[4] // 6.25)
        if data[5] == "centre":
            start_x = data[1][0]//2-text_surf.get_width()//2
        elif data[5] == "left":
            start_x = 0
        else:
            start_x = data[1][0]-text_surf.get_width()

        new_surf.blit(text_surf, (start_x, y))

        if len(parts) > 1:
            for num, part in enumerate(parts):
                if EMOJI_PATTERN.match(part):
                    x_pos = start_x + 15 + temp_font.size("".join(parts[:num]))[0]
                    img = c.image_store.icons[part]
                    new_surf.blit(scale_image(img,data[4]), (x_pos, y+8))
                    parts[num] = gap_size
        y += data[4]+5

    return new_surf
