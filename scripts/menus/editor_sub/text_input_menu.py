import pygame
from scripts import common as c
from scripts.editor_objects.button import Button
from scripts.utility.scale_image import scale_image
from scripts.menus.editor_sub.icon_selection import IconSelection
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
        self.icon_selection = IconSelection((c.width - 400, 70), None, width=330, height=300, submenu_layer=None,
                                            icon_size=30)

        self.line_no = 0
        self.icons_shown = False
        self.cursor_x, self.cursor_tick = len(self.lines[0]), 0
        self.backspace_tick = 35
        self.line_emojis = c.data["el"][c.selected[0]][10]

    def render(self):
        #   is called a 'three per em space'
        self.surf.fill((50, 50, 55))

        y = 20
        for line_no, line in enumerate(self.lines):
            cursor_offset = 0

            line2 = line.replace(" ", "   ")
            text_surf = c.editor_font.render(line2, True, (180, 180, 185))
            self.surf.blit(text_surf, (20, y))

            for emoji in self.line_emojis[line_no]:
                x = c.editor_font.size(line[:emoji[1]])[0]
                x += line[:emoji[1]].count(" ") * 1
                img = c.image_store.get_scaled_image(
                    "projects/" + c.project_name + "/images/" + emoji[0] + ".png", 20)
                if img is not None:
                    self.surf.blit(img, (20 + x, y + 4))

            if line_no == self.line_no:
                cursor_pos = self.cursor_x + cursor_offset
                if self.cursor_tick < 25:
                    size = c.editor_font.size(line[0:cursor_pos])[0]
                    size += line[:cursor_pos].count(" ") * 1
                    self.surf.blit(self.cursor, (20 + size, y))
            y += 35

        self.done_button.render(self.surf, (20, c.height - 150))
        self.icon_button.render(self.surf, (c.width - 240, c.height - 190))
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

        if self.icons_shown:
            self.icon_selection.render()

    def event(self, event):
        if self.icons_shown:
            output = self.icon_selection.event(event)
            if output is not None:
                print(output)
                line = self.lines[self.line_no]
                self.move_emojis_forwards()
                self.line_emojis[self.line_no].append([output, self.cursor_x])
                self.lines[self.line_no] = line[:self.cursor_x] + ' ' + line[self.cursor_x:]
                self.cursor_x += 1
                print(self.cursor_x, self.line_no)
                return

        if event.type == pygame.VIDEORESIZE:
            self.surf = pygame.Surface((c.width - 100, c.height - 100))
            self.done_button = Button("Done", width=c.width - 140)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - 50, event.pos[1] - 50)

            stop_others = False

            if event.button == 1:
                if not stop_others:
                    if self.done_button.click(event, pos):
                        c.data["el"][c.selected[0]][3] = "\n".join(self.lines)
                        c.data["el"][c.selected[0]][10] = self.line_emojis
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
                        line2 = re.sub(r"\bEMOJI-[\w|-]+", "  ", line)
                        self.cursor_x = len(line)

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
                    self.line_emojis.insert(0, [])
                else:
                    saved = self.lines[self.line_no][self.cursor_x:]
                    self.lines[self.line_no] = self.lines[self.line_no][:self.cursor_x:]

                    first_line, second_line = [], []

                    for num, emoji in enumerate(self.line_emojis[self.line_no]):
                        if emoji[1] >= self.cursor_x:
                            emoji = (emoji[0], emoji[1] - self.cursor_x)
                            second_line.append(emoji)
                        else:
                            first_line.append(emoji)

                    self.line_emojis[self.line_no] = second_line

                    self.line_no += 1
                    self.lines.insert(self.line_no, saved)
                    self.line_emojis.insert(0, first_line)
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
                    self.move_emojis_forwards()
                    self.lines[self.line_no] = line[:self.cursor_x] + event.unicode + line[self.cursor_x:]
                    self.cursor_x += 1

    def move_emojis_forwards(self):
        line = self.lines[self.line_no]
        if len(line) > 0:
            if self.cursor_x != len(line):
                for num, emoji in enumerate(self.line_emojis[self.line_no]):
                    if emoji[1] >= self.cursor_x:
                        self.line_emojis[self.line_no][num] = (emoji[0], emoji[1] + 1)

    def move_emojis_backwards(self):
        line = self.lines[self.line_no]
        if len(line) > 0:
            if self.cursor_x != len(line):
                for num, emoji in enumerate(self.line_emojis[self.line_no]):
                    if emoji[1] >= self.cursor_x:
                        self.line_emojis[self.line_no][num] = (emoji[0], emoji[1] - 1)

    def backspace(self):
        line = self.lines[self.line_no]
        if self.cursor_x == 0:
            if len(self.lines) != 1:
                stored_data = self.lines[self.line_no]
                stored_emojis = self.line_emojis[self.line_no].copy()
                del self.lines[self.line_no], self.line_emojis[self.line_no]
                if not self.line_no == 0:
                    self.line_no -= 1
                self.cursor_x = len(self.lines[self.line_no])
                self.lines[self.line_no] += stored_data

                for num, emoji in enumerate(stored_emojis):
                    stored_emojis[num] = (emoji[0], emoji[1] + self.cursor_x)
                self.line_emojis[self.line_no] += stored_emojis

        else:
            if self.cursor_x != 0:
                print(self.cursor_x)
                self.lines[self.line_no] = line[:self.cursor_x - 1] + line[self.cursor_x:]
                self.cursor_x = max(self.cursor_x - 1, 0)

                if line[self.cursor_x] == " ":
                    for num, emoji in enumerate(self.line_emojis[self.line_no]):
                        if emoji[1] == self.cursor_x:
                            del self.line_emojis[self.line_no][num]
                            print("Removed emoji " + emoji[0])
                            return

                self.move_emojis_backwards()
