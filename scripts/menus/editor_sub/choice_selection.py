import pygame
from scripts import common as c
from scripts.utility.file_manager import getFileList
from scripts.editor_objects.button import Button
from scripts.utility.scale_image import scale_image
from _thread import start_new_thread


class ChoiceSelection:
    def __init__(self, pos, path, set_path, width=300, allow_none=False, submenu_layer=1, icon_size=50):
        self.path, self.set_path, self.pos, self.allow_none, self.submenu_layer, self.icon_size = \
            path, set_path, pos, allow_none, submenu_layer, icon_size
        self.surf = pygame.Surface((width, 340), pygame.SRCALPHA)
        self.width = width

        if allow_none:
            self.none_button = Button("None", width=150)

        self.files = getFileList(path)
        self.icons = []
        start_new_thread(self.loadImages, ())

    def loadImages(self):
        # Used in a thread
        for file in self.files:
            if ".png" in file:
                img = pygame.image.load(self.path + "/" + file)
                img = scale_image(img, self.icon_size)
                self.icons.append(img)

    def render(self):
        self.surf.fill((50, 50, 55))
        x, y = (20, 20)
        if self.allow_none:
            self.none_button.render(self.surf, (self.width // 2 - 75, y))
            y += 40
        for icon in self.icons:
            self.surf.blit(icon, (x, y))
            x += self.icon_size + 10
            if x > self.width - self.icon_size:
                x = 20
                y += self.icon_size + 10

        c.display.blit(self.surf, self.pos)

    def event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = (self.pos[0] + 20, self.pos[1] + 20)
            if self.allow_none:
                m_pos = (event.pos[0] - self.pos[0], event.pos[1] - self.pos[1])
                if self.none_button.click(event, m_pos):
                    if len(self.set_path) == 4:
                        c.data["el"][self.set_path[0]][self.set_path[1]][self.set_path[2]][self.set_path[3]] = None
                    elif len(self.set_path) == 3:
                        c.data["el"][self.set_path[0]][self.set_path[1]][self.set_path[2]] = None
                    else:
                        c.data["el"][self.set_path[0]][self.set_path[1]] = None
                    c.menu.canvas.draw()
                    c.menu.side_bar.changeMenu()
                    if self.submenu_layer == 1:
                        c.submenu = None
                    else:
                        c.submenu2 = None
                y += 40
            for icon, file in zip(self.icons, self.files):
                rect = pygame.Rect(x, y, icon.get_width(), icon.get_height())

                if rect.collidepoint(event.pos):
                    if len(self.set_path) == 3:
                        c.data["el"][self.set_path[0]][self.set_path[1]][self.set_path[2]] = file.replace(".png", "")
                    elif len(self.set_path) == 4:
                        c.data["el"][self.set_path[0]][self.set_path[1]][self.set_path[2]][self.set_path[3]] = \
                            file.replace(".png", "")
                    else:
                        c.data["el"][self.set_path[0]][self.set_path[1]] = file.replace(".png", "")
                    c.menu.canvas.draw()
                    c.menu.side_bar.changeMenu()
                    if self.submenu_layer == 1:
                        c.submenu = None
                    else:
                        c.submenu2 = None
                x += self.icon_size + 10
                if x - self.pos[0] > self.width - self.icon_size:
                    x = self.pos[0] + 20
                    y += self.icon_size + 10
