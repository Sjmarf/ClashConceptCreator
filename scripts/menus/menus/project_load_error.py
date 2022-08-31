import pygame

from scripts import common as c
from scripts.editor_objects.button import Button


class ProjectLoadError:
    def __init__(self, ver="0", supported=""):
        rows = ["This project could not be loaded because it has an",
                "incompatible version number.",
                "",
                "Software version: " + c.VERSION,
                "Project version: " + ver,
                "Supported project versions: "+supported,
                "",
                "To open this project, you'll need to download a",
                "compatible version."]
        self.rows = []
        for row in rows:
            text_surf = c.editor_font.render(row, True, (200, 200, 205))
            self.rows.append(text_surf)

        self.download_button = Button("Download Latest Version", width=300)
        self.back_button = Button("Back", width=300)

    def render(self):
        c.display.fill((50, 50, 55))
        y = 80
        for row in self.rows:
            c.display.blit(row, (c.width // 2 - row.get_width() // 2, y))
            y += 35

        self.download_button.render(c.display,(c.width//2-150,y+50))
        self.back_button.render(c.display,(c.width//2-150,c.height-100))

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.click(event,event.pos):
                from scripts.menus.menus.main_menu import MainMenu
                c.menu = MainMenu()

            if self.download_button.click(event,event.pos):
                from webbrowser import open
                open('https://smarf1.itch.io/ccc')
