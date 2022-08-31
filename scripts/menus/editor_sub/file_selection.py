import pygame
from scripts import common as c
from scripts.utility.file_manager import getFileList
from _thread import start_new_thread


class FileSelection:
    def __init__(self, path, set_path):
        self.path, self.set_path = path, set_path
        self.surf = pygame.Surface((c.width - 100, c.height - 100), pygame.SRCALPHA)

        self.files = getFileList(path)
        self.icons = []
        start_new_thread(self.loadImages, ())

    def loadImages(self):
        # Used in a thread
        dark_bar = pygame.Surface((230, 30), pygame.SRCALPHA)
        dark_bar.fill((0, 0, 0, 180))
        for file in self.files:
            if ".png" in file:
                img = pygame.image.load(self.path + "/" + file)
                img = pygame.transform.smoothscale(img, (230, 128))
                img.blit(dark_bar, (0, 98))
                text_surf = c.editor_font.render(file.replace(".png", ""), True, (255, 255, 255))
                img.blit(text_surf, (115 - text_surf.get_width() // 2, 98))
                self.icons.append(img)

    def render(self):
        self.surf.fill((50, 50, 55))
        x, y = 20, 50
        for icon in self.icons:
            self.surf.blit(icon, (x, y))
            x += 250
            if x > 750:
                x = 20
                y += 148

        c.display.blit(self.surf, (50, 50))

    def event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.surf = pygame.Surface((c.width - 100, c.height - 100))

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - 50, event.pos[1] - 50)
            x, y = 20, 50
            for icon, file in zip(self.icons, self.files):
                rect = pygame.Rect(x, y, 230, 128)

                if rect.collidepoint(pos):
                    c.data["el"][self.set_path[0]][self.set_path[1]] = file.replace(".png", "")
                    c.menu.canvas.draw()
                    c.menu.side_bar.changeMenu()
                    c.submenu = None

                x += 250
                if x > 750:
                    x = 20
                    y += 148
