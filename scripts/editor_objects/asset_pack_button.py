import pygame
from scripts import common as c
from scripts.utility.scale_image import scale_image
from scripts.utility.file_manager import load_json

class AssetPackButton():
    def __init__(self, name, col=None, align="centre"):
        if col is None:
            if name == "Local":
                col = (155, 242, 114)
            elif name == "Clan Badge":
                col = (133, 114, 242)
            else:
                col = load_json('asset packs/' + name + '/search_data.json')["label_colour"]
        self.name = name
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
        if align == "centre":
            self.img.blit(text_surf, (110-text_surf.get_width()//2+10, 1))
        else:
            self.img.blit(text_surf, (35, 1))
        # Icon
        if name == "Local":
            icon = pygame.image.load('assets/editor_gui/local_icon.png').convert_alpha()
        elif name == "Clan Badge":
            icon = pygame.image.load('assets/editor_gui/clan_badge_icon.png').convert_alpha()
        else:
            icon = pygame.image.load('asset packs/' + name + '/icon.png').convert_alpha()
        icon = scale_image(icon, 20)
        if align == "centre":
            self.img.blit(icon, (110-text_surf.get_width()//2-20, 5))
        else:
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
