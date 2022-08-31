import pygame


class SmallButton:
    def __init__(self,icon="bin_button"):
        self.pos = (0,0)
        self.img = pygame.image.load('assets/editor_gui/'+icon+'.png').convert_alpha()

    def render(self, surf, pos):
        self.pos = pos
        surf.blit(self.img, pos)

    def click(self, event, pos) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rect = pygame.Rect(self.pos[0], self.pos[1], 30, 30)
                if rect.collidepoint(pos):
                    return True
