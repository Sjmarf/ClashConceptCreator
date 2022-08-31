from scripts import common as c
import pygame

from scripts.utility.file_manager import loadJson,saveJson,getFileList
from scripts.utility.size_element import size_element
from scripts.editor_objects.button import Button
from scripts.editor_objects.scrollbar import Scrollbar
from _thread import start_new_thread

class News:
    def __init__(self):
        self.title = c.editor_font_large.render("News", True, (250, 250, 255))
        self.news_error = c.editor_font_small.render("Error: news can't be updated automatically at this time.", True,
                                                     (255, 150, 150))
        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)

        self.articles,self.discord_buttons = [],[]
        self.fetching = False
        if c.menu.news_notif > 0:
            start_new_thread(self.fetch_new_news,())

        else:
            self.create_surfaces()

        self.scrollbar = Scrollbar()
        c.menu.news_notif = 0

    def fetch_new_news(self):
        self.fetching = True
        self.fetch_text = c.editor_font.render("Fetching news...", True,
                                                     (150, 150, 150))
        import requests
        url = "https://gist.githubusercontent.com/Sjmarf/85f99e730cfc3e16db535dc23d14d966/raw/ccc_news.json"
        response = requests.get(url=url,
                                headers={
                                    "Accept": "application/json"})

        new = response.json()
        saveJson('assets/reference/news/news.json',new)
        saveJson('data/last_news_id', c.menu.new_news_id)
        print("Saved new news")
        self.fetching = False
        self.create_surfaces()

    def create_surfaces(self):
        box = size_element('assets/editor_gui/main_menu/news.png', (c.width - 325, 200), (10, 10, 10, 10))
        cutout = pygame.image.load('assets/editor_gui/main_menu/news_cutout.png').convert_alpha()
        remove = pygame.Surface((200, 200), pygame.SRCALPHA)
        remove.fill((255, 255, 255, 255))
        fade = pygame.image.load('assets/editor_gui/gradient.png').convert_alpha()
        fade = pygame.transform.scale(fade, (30, 200))
        fade = pygame.transform.flip(fade, True, False)

        data = loadJson('assets/reference/news/news.json')
        self.articles = []
        self.discord_buttons = []

        for article in data:
            surf = box.copy()
            text_x = 0

            if article[0] is not None and article[0] in getFileList('assets/reference/news/'):
                surf.blit(remove, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
                img = pygame.image.load('assets/reference/news/' + article[0]).convert_alpha()
                img.blit(cutout, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
                surf.blit(img, (0, 0))
                surf.blit(fade, (200, 0))
                text_x = 215

            if article[4] == "DISCORD":
                self.discord_buttons.append((Button("",file="discord",width=150),
                                             c.DISCORD_LINK,text_x))
            else:
                self.discord_buttons.append((None,None,text_x))

            need_more_text = True
            max_width = c.width - 325 - text_x - 20
            text = article[2]
            text_index = 0
            text_y = 50
            # Loop each line
            while need_more_text:
                test_index = 0
                # Find the max number of words that fit on the line
                while need_more_text: # Loop through each word, break when it's too long
                    last_word_index = test_index
                    # Find the next space
                    while True:
                        test_index += 1
                        # Stop finding lines if we're at the end of the text
                        if test_index > len(text)-1:
                            need_more_text = False
                            break
                        # We've found a word!
                        if text[test_index] == " ":
                            break

                    # Remove the space at the start of the line

                    if c.editor_font_small.size(text[text_index:test_index])[0] > max_width:
                        test_index = last_word_index
                        if not need_more_text:
                            need_more_text = True
                        break

                line = text[text_index:test_index]
                if len(line) > 0:
                    if line[0] == " ":
                        line = line[1:]
                text_surf = c.editor_font_small.render(line,True,(200,200,205))
                surf.blit(text_surf,(text_x + 10, text_y))
                text_index = test_index
                text_y += 20

            title_surf = c.editor_font.render(article[1], True, (255, 255, 255))
            surf.blit(title_surf, (text_x + 10, 10))
            date_surf = c.editor_font_small.render(article[3], True, (150, 150, 155))
            surf.blit(date_surf, (c.width-335-date_surf.get_width(), 10))
            self.articles.append(surf)

    def render(self):
        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)
        centre = c.width // 2 - 125

        self.surf.blit(self.title, (centre - self.title.get_width() // 2, 15-self.scrollbar.scroll))
        y = 70-self.scrollbar.scroll

        if not c.menu.news_request_ok:
            self.surf.blit(self.news_error, (centre - self.news_error.get_width() // 2, 60 - self.scrollbar.scroll))
            y += 30

        if self.fetching:
            self.surf.blit(self.fetch_text, (centre - self.fetch_text.get_width() // 2, 60 - self.scrollbar.scroll))

        for button,article in zip(self.discord_buttons,self.articles):
            self.surf.blit(article, (25, y))
            if button[0] is not None:
                button[0].render(self.surf,(35+button[2],y+155))
            y += 225

        self.scrollbar.set_height(c.height-20,y+self.scrollbar.scroll)

        self.scrollbar.render(self.surf,(c.width-275,10))
        c.display.blit(self.surf, (250, 0))

    def event(self, event, pos):
        if event.type == pygame.VIDEORESIZE:
            self.create_surfaces()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.discord_buttons:
                if button[0] is not None:
                    if button[0].click(event,pos):
                        import webbrowser
                        webbrowser.open(button[1])

        self.scrollbar.event(event,pos)
