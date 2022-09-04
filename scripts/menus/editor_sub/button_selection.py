import pygame
from scripts import common as c
from scripts.utility.file_manager import get_file_list
from scripts.editor_objects.button import Button
from _thread import start_new_thread


class ButtonSelection:
    def __init__(self, pos, buttons, set_path, width=300, submenu_layer=1):
        self.pos, self.set_path, self.submenu_layer = pos, set_path, submenu_layer
        self.surf = pygame.Surface((width, len(buttons)*40+30), pygame.SRCALPHA)
        self.width = width

        self.buttons = []
        for button in buttons:
            self.buttons.append([Button(button, width=150), button])

    def render(self):
        self.surf.fill((50, 50, 55))
        x, y = (self.width // 2, 20)
        for button in self.buttons:
            button[0].render(self.surf, (x - 75, y))
            y += 40

        c.display.blit(self.surf, self.pos)

    def event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = (event.pos[0] - self.pos[0], event.pos[1] - self.pos[1])
            for button in self.buttons:
                if button[0].click(event,m_pos):
                    if self.submenu_layer == 1:
                        c.submenu = None
                    else:
                        c.submenu2 = None
                    if self.set_path is not None:
                        c.data["el"][self.set_path[0]][self.set_path[1]] = button[1]
                    else:
                        c.submenu_2_update_value = button[1]
                        c.submenu_2_update = True
                    c.menu.canvas.draw()
                    c.menu.side_bar.changeMenu()
