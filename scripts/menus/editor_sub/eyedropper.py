from scripts import common as c
import pygame

class Eyedropper:
    def __init__(self):
        self.canvas = pygame.transform.smoothscale(c.canvas,c.sizes["canvas"])
        self.size = c.sizes["canvas"]
        self.outline = pygame.Surface((c.sizes["canvas"][0]+10,c.sizes["canvas"][1]+10))
        self.outline.fill((255,255,255))

        self.preview = pygame.Surface((50,50),pygame.SRCALPHA)
        self.preview_outline = pygame.Surface((56, 56), pygame.SRCALPHA)
        self.preview_outline.fill((255,255,255))
        self.col = (0,0,0)

    def render(self):
        c.display.blit(self.outline,(0,0))
        c.display.blit(self.canvas,(0,0))
        mouse_x,mouse_y = pygame.mouse.get_pos()

        if 0 < mouse_x < self.size[0] and 0 < mouse_y < self.size[1]:
            self.col = self.canvas.get_at((mouse_x, mouse_y))
            self.preview.fill(self.col)

        c.display.blit(self.preview_outline, (mouse_x - 28, mouse_y + 52))
        c.display.blit(self.preview,(mouse_x-25,mouse_y+55))

    def event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                c.submenu_2_update_value = self.col
                c.submenu_2_update = True
                c.submenu2 = None