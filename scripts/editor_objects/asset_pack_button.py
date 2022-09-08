import pygame
from scripts import common as c
from scripts.utility.scale_image import scale_image

class AssetPackButton():
    def __init__(self, name, col):
        self.img = pygame.image.load('assets/editor_gui/button_black.png').convert_alpha()
        # Background
        col = pygame.Color(col)
        hsva = list(col.hsva)
        hsva[2] -= 30
        col.hsva = hsva
        self.img.fill(col, special_flags=pygame.BLEND_RGB_ADD)
        # Text
        col = pygame.Color(col)
        hsva = list(col.hsva)
        hsva[2] += 30
        hsva[1] = 20
        col.hsva = hsva
        text_surf = c.editor_font.render(name, True, col)
        self.img.blit(text_surf, (35, 1))  # 35+(80-text_surf.get_width()//2)
        # Icon
        icon = pygame.image.load('asset packs/' + name + '/icon.png').convert_alpha()
        icon = scale_image(icon, 20)
        self.img.blit(icon, (5, 5))
        self.pos = (0, 0)

    def render(self, surf, pos, alpha=255):
        self.pos = pos
        img = self.img.copy()
        img.set_alpha(alpha)
        surf.blit(img, pos)

    def click(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rect = pygame.Rect(self.pos[0], self.pos[1], 220, 30)
                if rect.collidepoint(pos):
                    return True
