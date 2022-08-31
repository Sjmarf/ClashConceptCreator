import pygame

from scripts import common as c
from scripts.utility.size_element import size_element


class Scrollbar:
    def __init__(self, height=200):
        self.scroll = 0
        self.max_scroll, self.height, self.slider_height = 100, 200, 100
        self.set_height(height, self.max_scroll)
        self.pos = (0, 0)
        self.picked_up = False
        self.show = False

    def set_height(self, height, max_scroll):
        if height != self.height or max_scroll != self.max_scroll:

            max_scroll -= height
            max_scroll += 50
            if max_scroll > 20:
                self.show = True
                self.height, self.max_scroll = height, max_scroll
                self.background = size_element('assets/editor_gui/scrollbar/background.png', (15, height), (0, 0, 10, 10))
                slider_height = int((height / max_scroll) * height)
                slider_height = max(20,slider_height)
                self.slider_height = slider_height
                self.slider = size_element('assets/editor_gui/scrollbar/slider.png', (15, slider_height), (0, 0, 10, 10))
            else:
                # Janky fix
                self.slider_height = self.height

    def render(self, surf, pos, mouse_y_offset=0):
        self.pos = pos
        if self.show:
            surf.blit(self.background, pos)
            if self.height < self.max_scroll:
                surf.blit(self.slider,
                          (pos[0], pos[1] + (self.scroll * (self.height - self.slider_height) / self.max_scroll)))
        mouse_y = pygame.mouse.get_pos()[1] - pos[1] - self.slider_height // 2 + mouse_y_offset
        if self.picked_up:
            self.scroll = mouse_y * self.max_scroll / (self.height - self.slider_height)
            self.scroll = max(0, min(self.max_scroll, self.scroll))

    def event(self, event, pos, scroll_rect=None):
        if event.type == pygame.MOUSEBUTTONUP:
            self.picked_up = False
        if scroll_rect is not None:
            if not scroll_rect.collidepoint(pos):
                return None
        if self.show:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    rect = pygame.Rect(self.pos[0], self.pos[1], 15, self.height)
                    if rect.collidepoint(pos):
                        self.picked_up = True

            elif event.type == pygame.MOUSEWHEEL:
                scroll = self.scroll-(event.y*20)
                self.scroll = max(0,min(self.max_scroll,scroll))

