import pygame
from scripts import common as c
from scripts.editor_objects.text_input import TextInput
from scripts.editor_objects.button import Button
from scripts.editor_objects.small_button import SmallButton


class StatListEditor:
    def __init__(self):
        self.surf = pygame.Surface((500, 430), pygame.SRCALPHA)
        self.data = c.data["el"][c.selected[0]][3]
        self.new_button = Button("New row",width=460)
        self.create_rows()

    def create_rows(self):
        self.rows = []
        for row in self.data:
            self.rows.append([
                TextInput(row[0], None, width=205),
                TextInput(row[1], None, width=205),
                SmallButton()
            ])

    def render(self):
        self.surf.fill((50, 50, 55))
        y = 20
        for row in self.rows:
            row[0].render(self.surf,(20, y))
            row[1].render(self.surf, (235, y))
            row[2].render(self.surf,(450,y))
            y += 40

        y += 10
        if len(self.data) < 10:
            self.new_button.render(self.surf,(20,y))

        c.display.blit(self.surf, (c.width // 2 - 250, c.height // 2 - 215))

    def event(self, event):
        pos = (0, 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - (c.width // 2 - 250), event.pos[1] - (c.height // 2 - 215))
            if len(self.data) < 10:
                if self.new_button.click(event,pos):
                    self.data.append(["",""])
                    self.create_rows()

        for num,row in enumerate(self.rows):
            if row[0].event(event,pos):
                self.data[num][0] = row[0].text
            if row[1].event(event,pos):
                self.data[num][1] = row[1].text
            if row[2].click(event,pos):
                del self.data[num]
                self.create_rows()
