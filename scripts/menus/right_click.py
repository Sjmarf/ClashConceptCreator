import pygame
from scripts import common as c

class RightClick:
    def __init__(self,options=["rename", "move", "delete"]):
        self.set_options(options,width=200, bg_col=(40,40,45))

    def set_options(self, options, width=200, bg_col=(40,40,45)):
        self.width = width
        self.surf = pygame.Surface((width, 20+(35*len(options))), pygame.SRCALPHA)
        self.surf.fill(bg_col)
        self.pos = (0, 0)
        self.options = options
        y = 10
        for option in self.options:
            text_surf = c.editor_font.render(option.title(), True, (200, 200, 205))
            self.surf.blit(text_surf, (10, y))
            y += 35

    def render(self, surf, pos):
        self.pos = pos
        surf.blit(self.surf, pos)

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in {1, 3}:
                rect = pygame.Rect(self.pos[0], self.pos[1], self.width, 300)

                if rect.collidepoint(event.pos):
                    mouse_pos = (event.pos[0] - self.pos[0], event.pos[1] - self.pos[1])

                    y = 10
                    for option in self.options:
                        rect = pygame.Rect(0, y, self.width, 35)
                        if rect.collidepoint(mouse_pos):
                            return option
                        y += 35
                else:
                    return True