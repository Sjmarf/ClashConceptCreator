from scripts import common as c
from scripts.editor_objects.button import Button
import pygame


class QuitConfirm:
    def __init__(self, quit_window=False):
        self.surf = pygame.Surface((400, 150), pygame.SRCALPHA)
        self.title = c.editor_font.render("Save changes?", True, (200, 200, 205))
        self.save_button = Button("Save", width=170)
        self.no_save_button = Button("Don't Save", width=170)
        self.quit_window = quit_window

    def render(self):
        self.surf.fill((50, 50, 55))
        self.surf.blit(self.title, (200 - self.title.get_width() // 2, 30))
        self.no_save_button.render(self.surf, (20, 100))
        self.save_button.render(self.surf, (210, 100))

        c.display.blit(self.surf, (c.width // 2 - 200, c.height // 2 - 75))

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - (c.width // 2 - 200), event.pos[1] - (c.height // 2 - 75))

            if self.no_save_button.click(event, pos):
                from scripts.menus.menus.main_menu import MainMenu
                self.quit()

            elif self.save_button.click(event, pos):
                c.menu.bottom_bar.save_project()
                self.quit()

    def quit(self):
        if self.quit_window:
            pygame.quit()
            raise SystemExit(0)
        else:
            from scripts.menus.menus.main_menu import MainMenu
            c.menu = MainMenu()
