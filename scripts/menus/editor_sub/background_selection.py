import pygame
from scripts import common as c
from scripts.utility.file_manager import getFileList
from scripts.editor_objects.button import Button
from _thread import start_new_thread


class BackgroundSelection:
    def __init__(self):
        self.surf = pygame.Surface((c.width - 100, c.height - 100), pygame.SRCALPHA)

        self.files = ["Home Village.png","Home Village2.png","Builder Base.png","Clan Capital.png","Capital Peak.png",
                      "Green.png",
                      "Blue-Green.png","Peaceful.png","Wood.png"]
        self.icons = {}
        self.page_icons = []
        self.page = 0
        self.icons_per_row = 3
        self.page_button = Button("Page: Clash of Clans",width=300)
        self.no_bg_button = Button("No background", width=300)
        start_new_thread(self.load_images, ())
        self.switch_page(0)

    def switch_page(self,page):
        self.page = page
        if page == 0:
            self.page_button = Button("Page: Clash of Clans", width=300)
            self.page_icons = ["Home Village.png","Home Village2.png","Builder Base.png","Clan Capital.png",
                               "Capital Peak.png"]
        else:
            self.page_button = Button("Page: Colours", width=300)
            self.page_icons = ["Green.png", "Blue-Green.png", "Peaceful.png", "Wood.png"]

    def load_images(self):
        # Used in a thread
        for file in self.files:
            if ".png" in file:
                img = pygame.image.load("assets/backgrounds/" + file)
                img = pygame.transform.smoothscale(img, (230, 128))
                self.icons[file] = img

    def render(self):
        self.surf.fill((50, 50, 55))
        self.page_button.render(self.surf,((c.width-100)//2-310,20))
        self.no_bg_button.render(self.surf, ((c.width - 100) // 2 + 10, 20))

        self.icons_per_row = (c.width-120)//250
        start_x = (c.width-120)//2-(self.icons_per_row*250)//2+20
        x, y = start_x, 80
        num = 0

        for icon in self.page_icons:
            if icon in self.icons.keys():
                self.surf.blit(self.icons[icon], (x, y))
                x += 250
                num += 1
                if num >= self.icons_per_row:
                    x = start_x
                    num = 0
                    y += 148

        c.display.blit(self.surf, (50, 50))

    def event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.surf = pygame.Surface((c.width - 100, c.height - 100))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = (event.pos[0] - 50, event.pos[1] - 50)
                if self.page_button.click(event,pos):
                    if self.page == 0:
                        self.switch_page(1)
                    else:
                        self.switch_page(0)

                elif self.no_bg_button.click(event,pos):
                    c.data["el"][c.selected[0]][3] = None
                    c.menu.canvas.draw()
                    c.menu.side_bar.changeMenu()
                    c.submenu = None

                start_x = (c.width - 120) // 2 - (self.icons_per_row * 250) // 2 + 20
                x, y = start_x, 80
                num = 0

                for icon in self.page_icons:
                    if icon in self.icons.keys():
                        rect = pygame.Rect(x,y,230,128)
                        if rect.collidepoint(pos):
                            c.data["el"][c.selected[0]][3] = icon.replace(".png","")
                            c.menu.canvas.draw()
                            c.menu.side_bar.changeMenu()
                            c.submenu = None
                        x += 250
                        num += 1
                        if num >= self.icons_per_row:
                            x = start_x
                            num = 0
                            y += 148
