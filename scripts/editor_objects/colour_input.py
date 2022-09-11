from scripts import common as c
from scripts.utility.spritesheet import SpriteSheet
from scripts.menus.editor_sub.colour_selection import ColourSelection
import pygame


class ColourInput:
    def __init__(self, colour, set_path, width=150, label=None, submenu_target=1, presets_list=()):

        self.submenu_target = submenu_target
        self.presets_list = presets_list

        src = pygame.image.load('assets/editor_gui/colour_select.png').convert_alpha()
        sheet = SpriteSheet(src, direct=True)
        img = pygame.Surface((width, 30), pygame.SRCALPHA)
        self.set_path = set_path

        if label is not None:
            self.HEIGHT = 60
            self.label_img = c.editor_font.render(label, True, (200, 200, 205))
        else:
            self.HEIGHT = 30
            self.label_img = None

        colour_surf = pygame.Surface((width - 10, 20), pygame.SRCALPHA)

        colour_surf.fill(colour)
        img.blit(colour_surf, (5, 5))
        mid = pygame.transform.scale(sheet.image((30, 0, 50, 30)), (width - 60, 30))
        img.blit(mid, (30, 0))
        img.blit(sheet.image((0, 0, 30, 30)), (0, 0))
        img.blit(sheet.image((80, 0, 30, 30)), (width - 30, 0))
        self.img = img

        self.pos = (0, 0)
        self.width = width
        self.colour = colour

    def render(self, surf, pos, centre=False):
        if centre:
            self.pos = (surf.get_width() // 2 - 75, pos[1])
        else:
            self.pos = pos

        if self.label_img is not None:
            surf.blit(self.label_img, self.pos)
            self.pos = (self.pos[0], self.pos[1] + 30)
        surf.blit(self.img, self.pos)

    def event(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rect = pygame.Rect(self.pos[0], self.pos[1], self.width, 30)
                if rect.collidepoint(pos):
                    menu = ColourSelection((c.width - 50 - 510, self.pos[1] + 40),
                                           self.colour, self.set_path, self.submenu_target,
                                           presets_list=self.presets_list)
                    if self.submenu_target == 1:
                        c.submenu = menu
                    elif self.submenu_target == 2:
                        c.submenu2 = menu
                    elif self.submenu_target == "main_menu":
                        c.menu.content.submenu = menu
                    return True
