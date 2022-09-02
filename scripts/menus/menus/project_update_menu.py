import pygame

from scripts import common as c
from scripts.editor_objects.button import Button
from scripts.utility.file_manager import loadJson


class ProjectUpdate:
    def __init__(self, name, ver="0"):
        self.project_name = name
        rows = ["This project was created on an older version",
                "of Clash Concept Creator (v"+ver+").",
                "",
                "Convert project to latest format (v"+c.VERSION+")?",
                "This action is irreversible, you might want",
                "to keep a copy of this project."]
        self.rows = []
        for row in rows:
            text_surf = c.editor_font.render(row, True, (200, 200, 205))
            self.rows.append(text_surf)

        self.img = pygame.image.load('assets/editor_gui/grand_builder.png').convert_alpha()
        self.convert_button = Button("Convert project", width=300)
        self.back_button = Button("< Back", width=100)

    def render(self):
        c.display.fill((50, 50, 55))
        c.display.blit(self.img,(c.width//2-75,30))

        y = 240
        for row in self.rows:
            c.display.blit(row, (c.width // 2 - row.get_width() // 2, y))
            y += 35

        self.back_button.render(c.display, (20, 20))
        self.convert_button.render(c.display,(c.width//2-150,y+50))

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.click(event,event.pos):
                from scripts.menus.menus.main_menu import MainMenu
                c.menu = MainMenu()

            if self.convert_button.click(event,event.pos):
                from scripts.utility.project_updater import update_project
                update_project(self.project_name)

                c.data = loadJson('projects/' + self.project_name + '/data.json')
                from scripts.menus.menus.editor import Editor
                c.menu = Editor()
