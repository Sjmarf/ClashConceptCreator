import pygame
from scripts import common as c
from scripts.utility.size_element import size_element
from scripts.editor_objects.button import Button
import copy


class ListLayoutEditor:
    def __init__(self):
        self.surf = pygame.Surface((c.width - 100, c.height - 100), pygame.SRCALPHA)
        self.buttons = [(Button("Add Text (1 line)", width=200), "text"),
                        (Button("Add Text (2 lines)", width=200), "double text"),
                        (Button("Add Image", width=200), "image"),
                        (Button("Add counter", width=200), "counter"),
                        (Button("Add readout", width=200), "readout")]
        self.done_button = Button("Done", width=c.width - 200)

        self.parts = copy.deepcopy(c.data["el"][c.selected[0]][3])
        self.checkbox = [pygame.image.load('assets/editor_gui/checkbox1.png').convert_alpha(),
                         pygame.image.load('assets/editor_gui/checkbox2.png').convert_alpha()]
        self.checkbox_coords = []

        self.picked_up, self.gap_moving, self.gap_start_x = None, None, 0
        self.cursor = pygame.Surface((1, 60), pygame.SRCALPHA)
        self.cursor.fill((255, 255, 255))
        self.create_surf()

    def create_surf(self):
        self.surf_width = max(700, c.width - 200)
        self.part_surf = pygame.Surface((self.surf_width, 100), pygame.SRCALPHA)
        self.gaps = [0]
        self.checkbox_coords = []
        mult = self.surf_width / 100
        x = 0
        for part in self.parts:
            img = size_element("assets/editor_gui/list/base.png", (part[1] * mult - 6, 60), (15, 15, 30, 30))
            text = part[0].title()
            if part[1] * mult - 6 < 60:
                text = text[0]
            text_surf = c.editor_font.render(text, True, (200, 200, 205))
            img.blit(text_surf, (img.get_width() // 2 - text_surf.get_width() // 2, 15))
            self.part_surf.blit(img, (x + 3, 0))
            self.gaps.append(x + part[1] * mult)
            x += part[1] * mult
            if x/mult != 100:
                if part[2]:
                    self.part_surf.blit(self.checkbox[1], (x - 15, 65))
                else:
                    self.part_surf.blit(self.checkbox[0],(x-15,65))
                self.checkbox_coords.append(x-15)

    def render(self):
        self.surf.fill((50, 50, 55))
        self.surf.blit(self.part_surf, (50, 50))

        y = 200
        for button in self.buttons:
            button[0].render(self.surf, (50, y))
            y += 40

        self.done_button.render(self.surf, (50, c.height - 160))

        if self.picked_up is not None:
            mouse_x = pygame.mouse.get_pos()[0] - 100
            pos = min(self.gaps, key=lambda m_x: abs(m_x - mouse_x))
            self.surf.blit(self.cursor, (49 + pos, 50))

        elif self.gap_moving is not None:
            pos = pygame.mouse.get_pos()[0] - 50
            self.surf.blit(self.cursor, (pos, 50))

        c.display.blit(self.surf, (50, 50))

    def event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.surf = pygame.Surface((c.width - 100, c.height - 100), pygame.SRCALPHA)
            self.done_button = Button("Done", width=c.width - 200)
            self.create_surf()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                pos = (event.pos[0] - 50, event.pos[1] - 50)
                rect = pygame.Rect((50, 50, c.width - 200, 60))
                if rect.collidepoint(pos) and len(self.gaps) > 2:
                    closest_gap = min(self.gaps[1:-1], key=lambda m_x: abs(m_x - (pos[0] - 50)))
                    if - 20 < pos[0] - 50 - closest_gap < 20:
                        self.gap_moving = self.gaps.index(closest_gap)
                        self.gap_start_x = closest_gap
                    else:
                        mult = (c.width - 200) / 100
                        x = 50
                        for num, part in enumerate(self.parts):
                            if x < pos[0] < x + part[1] * mult:
                                self.picked_up = num
                                break
                            x += part[1] * mult

                elif self.done_button.click(event, pos):

                    data = []
                    old_parts = c.data["el"][c.selected[0]][3]

                    # Loop through each row
                    for i, row_data in enumerate(c.data["el"][c.selected[0]][4]):
                        row = []
                        used_sections = []
                        # Loop through each slice (called a 'part') of the row
                        for num, part in enumerate(self.parts):
                            index = None
                            # Loop the old parts to find an unused match
                            for old_num, item in enumerate(old_parts):
                                if item[0] == part[0] and (old_num not in used_sections and num < len(row_data)):
                                    index = old_num
                                    break
                            if index is not None:
                                row.append(row_data[index])
                            else:
                                if part[0] == "text":
                                    row.append(["Text"])
                                elif part[0] == "image":
                                    row.append([None])
                                elif part[0] == "double text":
                                    row.append(["Text","Text"])
                                elif part[0] == "counter":
                                    row.append(["Text","0"])
                                elif part[0] == "readout":
                                    row.append(["0","trophy"])

                            used_sections.append(index)
                        data.append(row)

                    c.data["el"][c.selected[0]][4] = data
                    row = []
                    for part in self.parts:
                        if part[0] == "text":
                            row.append(["Text"])
                        elif part[0] == "image":
                            row.append([None])
                        elif part[0] == "double text":
                            row.append(["Text", "Text"])
                        elif part[0] == "counter":
                            row.append(["Text","0"])
                        elif part[0] == "readout":
                            row.append(["0", "trophy"])
                    c.data["el"][c.selected[0]][5] = row
                    c.data["el"][c.selected[0]][3] = self.parts
                    c.menu.canvas.draw()
                    c.submenu = None
                else:
                    y = 150
                    for button in self.buttons:
                        if button[0].click(event, pos):
                            index = None
                            threshold = 12
                            for part in range(len(self.parts)):
                                if self.parts[part][1] > threshold:
                                    index = part
                            if index is None:
                                print("Can't fit")
                            else:
                                half = self.parts[index][1] // 2
                                self.parts.append([button[1], half, True])
                                self.parts[index][1] -= half
                                self.create_surf()
                        y += 35

                    for num, x_pos in enumerate(self.checkbox_coords):
                        rect = pygame.Rect(50+x_pos,115,30,30)
                        if rect.collidepoint(pos):
                            self.parts[num][2] = not self.parts[num][2]
                            self.create_surf()
                            break

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = (event.pos[0] - 50, event.pos[1] - 50)
            x_pos = pos[0] - 50
            if self.picked_up is not None:
                bar_x = min(self.gaps, key=lambda m_x: abs(m_x - x_pos))
                index = self.gaps.index(bar_x)
                data = self.parts.pop(self.picked_up)
                if pos[1] > 200:
                    self.parts[self.picked_up - 1][1] += data[1]
                else:
                    self.parts.insert(index, data)
                self.create_surf()

            elif self.gap_moving is not None:
                diff = pos[0] - self.gap_start_x - 50
                diff = int(diff / ((c.width - 200) / 100))

                # Stops a part from being too small
                # threshold = int(67 / ((c.width - 200) / 100)) + 1
                threshold = 6

                if self.parts[self.gap_moving][1] - diff < threshold:
                    diff -= (threshold - (self.parts[self.gap_moving][1] - diff))

                if self.parts[self.gap_moving - 1][1] + diff < threshold:
                    diff += (threshold - (self.parts[self.gap_moving - 1][1] + diff))

                self.parts[self.gap_moving][1] -= diff
                self.parts[self.gap_moving - 1][1] += diff

                self.create_surf()

            self.picked_up, self.gap_moving = None, None
