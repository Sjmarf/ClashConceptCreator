import pygame
from scripts import common as c


def text_lines(text, width, font_size="small"):
    need_more_text = True
    if font_size == "small":
        font = c.editor_font_small
    lines = []
    text_index = 0
    # Loop each line
    while need_more_text:
        test_index = 0
        # Find the max number of words that fit on the line
        while need_more_text:  # Loop through each word, break when it's too long
            last_word_index = test_index
            # Find the next space
            while True:
                test_index += 1
                # Stop finding lines if we're at the end of the text
                if test_index > len(text) - 1:
                    need_more_text = False
                    break
                # We've found a word!
                if text[test_index] == " ":
                    break

            # Remove the space at the start of the line

            if font.size(text[text_index:test_index])[0] > width:
                test_index = last_word_index
                if not need_more_text:
                    need_more_text = True
                break

        line = text[text_index:test_index]
        if len(line) > 0:
            if line[0] == " ":
                line = line[1:]
        text_surf = font.render(line, True, (200, 200, 205))
        lines.append(text_surf)
        text_index = test_index

    surf = pygame.Surface((width,len(lines)*20),pygame.SRCALPHA)
    y = 0
    for line in lines:
        surf.blit(line,(0,y))
        y += 20
    return surf
