import pygame

from scripts import common as c
from scripts.editor_objects.button import Button
from scripts.utility.file_manager import save_json_base_design


class BottomBar:
    def __init__(self):
        self.surf = pygame.Surface((c.width, 200), pygame.SRCALPHA)

        self.add_button = Button("Add", width=150)
        self.save_button = Button("Save", width=150)
        self.export_button = Button("Export", width=150)
        self.quit_button = Button("Quit", width=150)

    def render(self):
        self.surf.fill((40, 40, 45))

        self.add_button.render(self.surf, (10, 10))
        self.save_button.render(self.surf, (10, 70))
        self.export_button.render(self.surf, (10, 110))
        self.quit_button.render(self.surf, (10, 150))

        fps_text = c.editor_font.render(str(c.fps), True, (100, 100, 105))
        self.surf.blit(fps_text, (c.width - 10 - fps_text.get_width(), 10))

        c.display.blit(self.surf, (0, c.height - 200))

    def event(self, event):
        pos = (0,0)
        if event.type == pygame.VIDEORESIZE:
            self.surf = pygame.Surface((c.width, 200), pygame.SRCALPHA)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0],event.pos[1]-c.height+200)

        if self.quit_button.click(event,pos):
            from scripts.menus.menus.main_menu import MainMenu
            c.menu = MainMenu()

        if self.add_button.click(event,pos):
            c.menu.board.new_building = not c.menu.board.new_building

        if self.save_button.click(event,pos):
            save_json_base_design('projects/'+c.project_name+"/data.json",c.data)
            print("Saved")
