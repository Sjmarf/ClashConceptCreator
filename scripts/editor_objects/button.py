from scripts import common as c
from scripts.utility.spritesheet import SpriteSheet
import pygame


class Button:
    def __init__(self, text, width=None, pos=(0, 0), file='blank', text_col=(200, 200, 205)):
        text = c.editor_font.render(text, True, text_col)
        if width is None:
            width = text.get_width() + 30
        self.width = width

        files = {"blank":'assets/editor_gui/button.png',
                 "discord":'assets/editor_gui/discord_button.png',
                 "itch":'assets/editor_gui/button_green.png'}

        if file in {"blank","itch"}:
            src = pygame.image.load(files[file]).convert_alpha()
            sheet = SpriteSheet(src, direct=True)
            img = pygame.Surface((width, 30), pygame.SRCALPHA)

            mid = pygame.transform.scale(sheet.image((30, 0, 50, 30)), (width - 60, 30))
            img.blit(mid, (30, 0))
            img.blit(sheet.image((0, 0, 30, 30)), (0, 0))
            img.blit(sheet.image((80, 0, 30, 30)), (width - 30, 0))
            img.blit(text, (width // 2 - text.get_width() // 2, 1))
            self.img = img
        else:
            self.img = pygame.image.load(files[file]).convert_alpha()
        self.pos = pos
        # self.img = pygame.transform.smoothscale(img,(img.get_width()//2,30))

    def render(self, surf, pos=None):
        if pos is not None:
            self.pos = pos
        surf.blit(self.img, self.pos)

    def click(self, event, pos) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rect = pygame.Rect(self.pos[0], self.pos[1], self.width, 30)
                if rect.collidepoint(pos):
                    return True
