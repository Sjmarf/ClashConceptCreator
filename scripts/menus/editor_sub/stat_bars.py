import pygame
from scripts import common as c
from scripts.editor_objects.text_input import TextInput
from scripts.editor_objects.choice_input import ChoiceInput
from scripts.editor_objects.button import Button
from scripts.editor_objects.small_button import SmallButton


class StatBarsEditor:
    def __init__(self):
        self.surf = pygame.Surface((620, 430), pygame.SRCALPHA)
        self.data = c.data["el"][c.selected[0]][3]
        self.new_button = Button("New bar",width=580)
        self.create_rows()
        self.reloaded = False

    def create_rows(self):
        self.rows = []
        for num,row in enumerate(self.data):
            self.rows.append([
                ChoiceInput(row[0], [c.selected[0], 3, num, 0], 'assets/elements/icon',
                            window_width=600, allow_none=True, submenu_layer=2, icon_size=30),
                TextInput(row[1], None, width=200),
                TextInput(str(row[2]), None, width=80, int_only=True, int_min=0, convert_int=True),
                TextInput(str(row[3]), None, width=80, int_only=True, int_min=0, convert_int=True),
                SmallButton()
            ])

    def render(self):
        self.surf.fill((50, 50, 55))
        y = 20
        for row in self.rows:
            row[0].render(self.surf,(20, y))
            row[1].render(self.surf, (180, y))
            row[2].render(self.surf,(390,y))
            row[3].render(self.surf, (480, y))
            row[4].render(self.surf, (570, y))
            y += 40

        y += 10
        if len(self.data) < 10:
            self.new_button.render(self.surf,(20,y))

        c.display.blit(self.surf, (c.width // 2 - 310, c.height // 2 - 215))

        if c.submenu2 is None and not self.reloaded:
            self.reloaded = True
            self.create_rows()
        elif c.submenu2 is not None:
            self.reloaded = False

    def event(self, event):
        pos = (0, 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - (c.width // 2 - 310), event.pos[1] - (c.height // 2 - 215))
            if len(self.data) < 10:
                if self.new_button.click(event,pos):
                    self.data.append([None,"","0","100"])
                    self.create_rows()

        for num,row in enumerate(self.rows):
            row[0].window_pos_x = c.width//2-420
            row[0].event(event,pos)
            if row[1].event(event,pos):
                self.data[num][1] = row[1].text
            if row[2].event(event,pos):
                self.data[num][2] = row[2].text
            if row[3].event(event,pos):
                self.data[num][3] = row[3].text
            if row[4].click(event,pos):
                del self.data[num]
                self.create_rows()
