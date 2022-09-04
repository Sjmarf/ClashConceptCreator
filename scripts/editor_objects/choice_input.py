import pygame
from scripts import common as c
from scripts.utility.size_element import size_element

class ChoiceInput:
    def __init__(self, text, setting_path, asset_path, label=None, window_width=200, allow_none=False, mode="images",
                 submenu_layer=1, icon_size=50, window_x=None, width=150):
        # 'Mode' dictates whether it should be a list of buttons or icons
        self.img, self.pos = None, (0, 0)
        self.asset_path, self.setting_path, self.mode = asset_path, setting_path, mode
        self.window_width, self.allow_none, self.submenu_layer, self.icon_size = window_width, allow_none, \
                                                                                 submenu_layer, icon_size
        self.width = width
        self.HEIGHT = 30
        if window_x is None:
            self.window_pos_x = c.width - 50 - self.window_width
        else:
            self.window_pos_x = window_x
        self.createSurface(text)
        if label is not None:
            self.HEIGHT = 60
            self.label_img = c.editor_font.render(label, True, (200, 200, 205))
        else:
            self.HEIGHT = 30
            self.label_img = None

        self.waiting_for_update = False

    def createSurface(self, text):
        self.text = text
        self.img = size_element('assets/editor_gui/choice_input.png',(self.width,30),(5,35,5,5))
        # Load text
        raw_text_surf = c.editor_font.render(text, True, (200, 200, 205))
        text_surf = pygame.Surface((self.width-40, 30), pygame.SRCALPHA)
        text_surf.blit(raw_text_surf, (0, 0))
        fade = pygame.image.load('assets/editor_gui/text_fade.png').convert_alpha()
        text_surf.blit(fade, (self.width-70, 0), special_flags=pygame.BLEND_RGBA_SUB)

        self.img.blit(text_surf, (5, 1))

    def render(self, surf, pos, centre=False):
        img = self.img
        if centre:
            self.pos = (surf.get_width() // 2 - 75, pos[1])
        else:
            self.pos = pos

        if self.label_img is not None:
            surf.blit(self.label_img, self.pos)
            self.pos = (self.pos[0], self.pos[1] + 30)

        surf.blit(img, self.pos)

        if self.waiting_for_update and c.submenu_2_update:
            self.createSurface(c.submenu_2_update_value)
            self.waiting_for_update = False

        elif c.submenu2 is None:
            self.waiting_for_update = False

    def event(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            rect = pygame.Rect((self.pos[0] + self.width - 30, self.pos[1], 30, 30))
            if rect.collidepoint(pos):
                if self.asset_path == 'all_images':
                    pass
                else:
                    if self.mode == "images":
                        from scripts.menus.editor_sub.icon_selection import IconSelection
                        selection = IconSelection((self.window_pos_x, self.pos[1] + 40),
                                                  self.setting_path, width=self.window_width,
                                                  submenu_layer=self.submenu_layer,
                                                  icon_size=self.icon_size)

                    else:
                        from scripts.menus.editor_sub.button_selection import ButtonSelection
                        selection = ButtonSelection((self.window_pos_x, self.pos[1] + 40),
                                                    self.asset_path, self.setting_path, width=self.window_width,
                                                    submenu_layer=self.submenu_layer)

                    if self.submenu_layer == 1:
                        c.submenu = selection
                    else:
                        c.submenu2 = selection

                    self.waiting_for_update = True
