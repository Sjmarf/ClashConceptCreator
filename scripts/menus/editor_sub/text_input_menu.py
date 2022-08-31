import pygame
from scripts import common as c
from scripts.editor_objects.button import Button
from scripts.utility.scale_image import scale_image
import re


class TextInputMenu:
    def __init__(self):
        self.surf = pygame.Surface((c.width - 100, c.height - 100), pygame.SRCALPHA)
        self.text = c.data["el"][c.selected[0]][3]
        self.lines = self.text.split("\n")
        self.cursor = pygame.Surface((1, 25), pygame.SRCALPHA)
        self.cursor.fill((255, 255, 255))
        self.done_button = Button("Done", width=c.width - 140)
        self.icon_button = Button("Icons", width=120)

        self.line_no = 0
        self.icons_shown = False
        self.cursor_x, self.cursor_tick = len(self.lines[0]), 0
        self.backspace_tick = 35

        self.EMOJI_PATTERN = re.compile(
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

    def render(self):
        self.surf.fill((50, 50, 55))
        if self.icons_shown:
            x, y = c.width-150, c.height - 240
            for icon in c.image_store.icons.values():
                icon = scale_image(icon,30)
                self.surf.blit(icon,(x,y))
                y -= 35
                if y < 100:
                    y = c.height - 240
                    x -= 35

        y = 20
        for line_no, line in enumerate(self.lines):
            parts = re.split(self.EMOJI_PATTERN, line)  # https://www.thisdot.co/blog/understanding-regex
            line2 = re.sub(self.EMOJI_PATTERN, "   ", line)
            cursor_offset = 0
            characters_moved = 0

            text_surf = c.editor_font.render(line2, True, (180, 180, 185))
            self.surf.blit(text_surf, (20, y))

            for num, part in enumerate(parts):
                if self.EMOJI_PATTERN.match(part):
                    parts[num] = "   "
                    x = c.editor_font.size("".join(parts[0:num]))[0] + 20
                    img = c.image_store.icons[part]
                    self.surf.blit(scale_image(img,20), (x, y+4))
                    if characters_moved < self.cursor_x:
                        cursor_offset -= 1
                        cursor_offset += 3
                    characters_moved += 1
                else:
                    characters_moved += len(part)

            if line_no == self.line_no:
                cursor_pos = self.cursor_x + cursor_offset
                if self.cursor_tick < 25:
                    size = c.editor_font.size(line2[0:cursor_pos])[0]
                    self.surf.blit(self.cursor, (20 + size, y))
            y += 35

        self.done_button.render(self.surf, (20, c.height - 150))
        self.icon_button.render(self.surf, (c.width-240,c.height-190))
        c.display.blit(self.surf, (50, 50))

        self.cursor_tick += 1
        if self.cursor_tick == 50:
            self.cursor_tick = 0

        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            self.backspace_tick -= 60 / c.fps
            if self.backspace_tick < 0:
                self.backspace_tick = 5
                self.backspace()
        else:
            self.backspace_tick = 35

    def event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.surf = pygame.Surface((c.width - 100, c.height - 100))
            self.done_button = Button("Done", width=c.width - 140)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - 50, event.pos[1] - 50)

            stop_others = False
            if self.icons_shown:
                x,y = c.width - 150,c.height - 240
                for emoji in c.image_store.icons.keys():
                    rect = pygame.Rect((x, y, 30, 30))
                    if rect.collidepoint(pos):
                        line = self.lines[self.line_no]
                        self.lines[self.line_no] = line[:self.cursor_x] + emoji + line[self.cursor_x:]
                        self.cursor_x += 1
                        stop_others = True
                        break
                    y -= 35
                    if y < 100:
                        y = c.height - 240
                        x -= 35

            if not stop_others:
                if self.done_button.click(event, pos):
                    c.data["el"][c.selected[0]][3] = "\n".join(self.lines)
                    c.menu.canvas.draw()
                    c.submenu = None

                elif self.icon_button.click(event, pos):
                    self.icons_shown = not self.icons_shown

                else:
                    # Set line number to mouse y
                    self.line_no = max(0, min(((pos[1] - 20) // 35), len(self.lines) - 1))
                    # Set cursor x to mouse x
                    mouse_pos_x = pos[0] - 20
                    line = self.lines[self.line_no]
                    self.cursor_x = len(line)
                    line2 = re.sub(self.EMOJI_PATTERN, " ", line)

                    for char_num in range(0, len(line2)):
                        char_offset = c.editor_font.size(line2[:char_num])[0]
                        if char_offset >= mouse_pos_x - 10:
                            self.cursor_x = char_num
                            break

        elif event.type == pygame.KEYDOWN:
            line = self.lines[self.line_no]
            if event.key == pygame.K_RETURN:
                if self.cursor_x == 0 and len(line) != 0 and self.line_no == 0:
                    self.lines.insert(0, "")
                else:
                    saved = self.lines[self.line_no][self.cursor_x:]
                    self.lines[self.line_no] = self.lines[self.line_no][:self.cursor_x:]
                    self.line_no += 1
                    self.lines.insert(self.line_no, saved)
                self.cursor_x = 0

            elif event.key == pygame.K_RIGHT:
                self.cursor_x = min(self.cursor_x + 1, len(line))

            elif event.key == pygame.K_LEFT:
                self.cursor_x = max(self.cursor_x - 1, 0)

            elif event.key == pygame.K_UP:
                self.line_no = max(self.line_no - 1, 0)
                self.cursor_x = len(self.lines[self.line_no])

            elif event.key == pygame.K_DOWN:
                self.line_no = min(self.line_no + 1, len(self.lines) - 1)
                self.cursor_x = len(self.lines[self.line_no])

            elif event.key == pygame.K_BACKSPACE:
                self.backspace()

            else:
                # This if-statement prevents keys that don't have unicode from messing it up
                if event.unicode != "":
                    self.lines[self.line_no] = line[:self.cursor_x] + event.unicode + line[self.cursor_x:]
                    self.cursor_x += 1

    def backspace(self):
        line = self.lines[self.line_no]
        if self.cursor_x == 0:
            if len(self.lines) != 1:
                stored_data = self.lines[self.line_no]
                del self.lines[self.line_no]
                if not self.line_no == 0:
                    self.line_no -= 1
                self.cursor_x = len(self.lines[self.line_no])
                self.lines[self.line_no] += stored_data

        else:
            if self.cursor_x != 0:
                self.lines[self.line_no] = line[:self.cursor_x - 1] + line[self.cursor_x:]
                self.cursor_x = max(self.cursor_x - 1, 0)
