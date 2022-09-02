import pygame
from scripts import common as c
from scripts.utility.file_manager import getFileList
from scripts.editor_objects.button import Button


class ButtonTypeSelector:
    def __init__(self):
        self.surf = pygame.Surface((280, 500), pygame.SRCALPHA)
        self.surf.fill((50, 50, 55))
        self.buttons = [["green", "red", "blue", "light blue", "dark blue", "lilac", "beige", "orange"],
                        ["orange2", "orange3", "capital white", "capital beige", "capital green", "capital blue",
                         "custom"]]

        x, y = 20, 20
        for column in self.buttons:
            for button in column:
                img = pygame.image.load('assets/elements/button/' + button + '.png').convert_alpha()
                img = pygame.transform.smoothscale(img, (110, 50))
                self.surf.blit(img, (x, y))
                y += 60
            y = 20
            x += 130

        self.small_icons = [["info", "drop-down", "more", "small"], ["view", "war-info","profile","play"]]

        x, y = 150, 440
        for row in self.small_icons:
            for button in row:
                img = pygame.image.load('assets/elements/button/' + button + '.png').convert_alpha()
                img = pygame.transform.smoothscale(img, (20, 20))
                self.surf.blit(img, (x, y))
                x += 30
            x = 150
            y += 30

    def render(self):
        c.display.blit(self.surf, (c.width - 300, 50))

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - (c.width - 300), event.pos[1] - 50)
            x, y = 20, 20
            for column in self.buttons:
                for button in column:
                    rect = pygame.Rect(x, y, 110, 50)
                    if rect.collidepoint(pos):
                        self.switch(button)
                        return
                    y += 60
                y = 20
                x += 130

            x, y = 150, 440
            for row in self.small_icons:
                for button in row:
                    rect = pygame.Rect(x, y, 20, 20)
                    if rect.collidepoint(pos):
                        self.switch(button)
                        return
                    x += 30
                x = 150
                y += 30

    def switch(self, button):
        c.data["el"][c.selected[0]][3] = button
        c.menu.side_bar.changeMenu()
        c.menu.canvas.draw()
        c.submenu = None
