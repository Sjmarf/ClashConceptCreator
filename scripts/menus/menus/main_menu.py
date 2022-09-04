import pygame

from scripts import common as c
from scripts.utility import font
from scripts.utility.scale_image import scale_image
from scripts.menus.main_menu_sub.projects import Projects
from scripts.menus.main_menu_sub.images import Images
from scripts.menus.main_menu_sub.news import News
from scripts.menus.main_menu_sub.reddit import Reddit
from scripts.menus.main_menu_sub.settings import Settings
from scripts.menus.main_menu_sub.about import About
import requests
from _thread import start_new_thread
from scripts.utility.file_manager import load_json, save_json


class SidebarButton:
    def __init__(self, text):
        self.surf = pygame.Surface((250, 40), pygame.SRCALPHA)
        self.surf.fill((80, 80, 85))
        self.text_surf = c.editor_font.render(text, True, (200, 200, 205))
        self.text_surf2 = c.editor_font.render(text, True, (255, 255, 255))

        self.pos = (0, 0)

    def render(self, surf, pos, highlighted):
        self.pos = pos
        if highlighted:
            self.surf.fill((236, 121, 117))
            self.surf.blit(self.text_surf2,
                           (125 - self.text_surf2.get_width() // 2, 19 - self.text_surf2.get_height() // 2))
        else:
            rect = pygame.Rect(self.pos[0], self.pos[1], 250, 40)
            mouse = pygame.mouse.get_pos()
            if rect.collidepoint(mouse):
                self.surf.fill((90, 90, 95))
            else:
                self.surf.fill((80, 80, 85))

            self.surf.blit(self.text_surf,
                           (125 - self.text_surf.get_width() // 2, 19 - self.text_surf.get_height() // 2))
        surf.blit(self.surf, pos)

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rect = pygame.Rect(self.pos[0], self.pos[1], 250, 40)
                if rect.collidepoint(event.pos):
                    return True


class MainMenu:
    def __init__(self,tab=0):
        self.news_request_ok, self.news_notif, self.new_news_id, self.checked_for_news = True, 0, 0, False

        self.logo_img = pygame.image.load('assets/editor_gui/main_menu/logo.png').convert_alpha()
        self.notif_img = pygame.image.load('assets/editor_gui/main_menu/notification.png').convert_alpha()
        self.tab = tab
        pages = [Projects, Images, News, Reddit, Settings, About]
        self.content = pages[tab]()
        self.create_surfaces()

        self.sidebar_buttons = [SidebarButton("Projects"),
                                SidebarButton("Images"),
                                SidebarButton("News"),
                                SidebarButton("Reddit"),
                                SidebarButton("Settings"),
                                SidebarButton("About")]

    def check_for_news_updates(self):
        # Increment the value at this site by 1 when you add news!
        url = "https://gist.githubusercontent.com/Sjmarf/85f99e730cfc3e16db535dc23d14d966/raw/ccc_news_id.json"
        try:
            response = requests.get(url=url,
                                    headers={
                                        "Accept": "application/json"})
        except requests.exceptions.ConnectionError:
            print("ConnectionError when loading news ID")
            c.menu.news_request_ok = False

        if type(c.menu).__name__ == "MainMenu":
            if c.menu.news_request_ok:
                if not response.ok:
                    c.menu.news_request_ok = False
                    print('Error loading news ID')
                else:
                    new_id = response.json()
                    print("Loaded news id")
                    old_id = load_json('data/last_news_id')
                    if old_id != new_id:
                        print("New news! ID:",new_id)
                        self.news_notif = new_id - old_id
                        self.new_news_id = new_id
                        if self.tab == 2:  # If the user clicked on news faster than we loaded the notif, reload news
                            self.content = News()

    def create_surfaces(self):
        self.sidebar = pygame.Surface((250, c.height), pygame.SRCALPHA)
        img = pygame.image.load('assets/editor_gui/gradient.png').convert_alpha()
        img = pygame.transform.flip(img, True, False)
        self.gradient_img = pygame.transform.scale(img, (30, c.height))

    def render(self):
        if not self.checked_for_news:
            start_new_thread(self.check_for_news_updates, ())
            self.checked_for_news = True

        c.display.fill((50, 50, 55))
        self.sidebar.fill((70, 70, 75))
        self.sidebar.blit(self.logo_img, (25, 25))
        y = 250
        for num, button in enumerate(self.sidebar_buttons):
            button.render(self.sidebar, (0, y), num == self.tab)
            if num == 2 and self.news_notif > 0:
                self.sidebar.blit(self.notif_img, (215, y + 5))
                text_surf = c.editor_font_small.render(str(self.news_notif), True, (255, 255, 255))
                self.sidebar.blit(text_surf, (230 - text_surf.get_width() // 2, y + 9))
            y += 50

        c.display.blit(self.sidebar, (0, 0))
        if self.content is not None:
            self.content.render()

        c.display.blit(self.gradient_img, (250, 0))

    def event(self, event):
        pos = (0, 0)
        if event.type == pygame.VIDEORESIZE:
            self.create_surfaces()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Sidebar tabs
            for num, button in enumerate(self.sidebar_buttons):
                if button.event(event):
                    self.tab = num
                    self.content = None
                    pages = [Projects, Images, News, Reddit, Settings, About]
                    if pages[self.tab] is not None:
                        self.content = pages[self.tab]()

        if event.type in {pygame.MOUSEBUTTONDOWN,pygame.MOUSEWHEEL}:
            pos = pygame.mouse.get_pos()
            pos = (pos[0] - 250, pos[1])

        if self.content is not None:
            self.content.event(event, pos)
