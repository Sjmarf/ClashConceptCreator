import pygame
from scripts import common as c


class SpriteSheet():

    def __init__(self, filename, scale=1, direct=False):
        if direct:
            self.sheet = filename

        else:
            try:
                self.sheet = pygame.image.load(filename).convert_alpha()
                self.sheet = pygame.transform.scale(self.sheet,
                                                    (self.sheet.get_width() * scale, self.sheet.get_height() * scale))

            except pygame.error as e:
                print(f"Unable to load spritesheet image: {filename}")
                raise SystemExit(e)

    def image(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def getWidth(self):
        return self.sheet.get_width()
