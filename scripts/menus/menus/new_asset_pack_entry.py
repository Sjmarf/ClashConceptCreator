import pygame

from scripts import common as c
from scripts.editor_objects.text_input import TextInput
from scripts.editor_objects.button import Button
from scripts.utility.file_manager import load_json,special_indent_save_json
from scripts.utility.scale_image import scale_image
import requests
import io
from _thread import start_new_thread


class NewAssetPackEntry:
    def __init__(self, pack):
        self.pack = pack
        self.data = load_json('asset packs/' + pack + '/search_data.json')
        self.image_json = load_json('asset packs/' + pack + '/images.json')
        self.back_button = Button("< Back", width=100)
        self.title = c.editor_font.render("New image for " + pack, True, (200, 200, 205))
        self.url_input = TextInput("", None, width=c.width - 160, empty="url", no_editor=True)
        self.name_input = TextInput("", None, width=300, empty="name", no_editor=True)
        self.add_button = Button("Add", width=300)
        self.clear_button = Button("Clear", width=100)
        self.suggestion_button = Button("", width=300)
        self.url = None
        self.suggestion = None
        self.url_surf = None
        self.url_valid = False
        self.preview_surf = pygame.Surface((200, 200), pygame.SRCALPHA)

    def render(self):
        c.display.fill((50, 50, 55))
        c.display.blit(self.title, (c.width // 2 - self.title.get_width() // 2, 20))
        self.back_button.render(c.display, (20, 20))

        self.url_input.render(c.display, (25, 100))
        self.clear_button.render(c.display, (c.width - 125, 100))
        if self.url is not None:
            c.display.blit(self.url_surf, (c.width // 2 - self.url_surf.get_width() // 2, 150))
            c.display.blit(self.preview_surf, (c.width // 2 - 100, 200))
            if self.url_valid:
                y = 430
                if self.suggestion is not None:
                    self.suggestion_button.render(c.display, (c.width // 2 - 150, 430))
                    y = 470
                self.name_input.render(c.display,(c.width//2-150,y))
                self.add_button.render(c.display,(c.width//2-150,y+40))

    def event(self, event):
        pos = (0, 0)

        if event.type == pygame.VIDEORESIZE:
            self.url_input = TextInput(self.url_input.text, None, width=c.width - 160, empty="url", no_editor=True)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if self.back_button.click(event, event.pos):
                from scripts.menus.menus.asset_packs import AssetPacks
                c.menu = AssetPacks()

            elif self.clear_button.click(event, event.pos):
                self.url_input = TextInput("", None, width=c.width - 160, empty="url", no_editor=True)
                self.url = None

            elif self.suggestion is not None:
                if self.suggestion_button.click(event,pos):
                    self.name_input = TextInput(self.suggestion, None, width=300, empty="name", no_editor=True)

        output = self.url_input.event(event, pos)
        if output:
            url = self.url_input.text
            url = url.replace(self.data["prefix"], "")
            self.url = url.replace(self.data["suffix"], "")

            full_url = self.url_input.text
            if '/revision/latest' in self.url:
                self.url = self.url.split('/revision/latest')[0]
                full_url = full_url.split('/revision/latest')[0]

            self.url_surf = c.editor_font.render(self.url, True, (170, 255, 150))
            start_new_thread(self.load_image_thread, (full_url,))

        if self.url is not None and self.url_valid:
            self.name_input.event(event,pos)
            if self.add_button.click(event,pos):

                if self.name_input.text.lower() in self.image_json.keys():
                    self.url_surf = c.editor_font.render("Key already in use", True, (255, 150, 150))
                else:
                    self.image_json[self.name_input.text.lower()] = self.url
                    special_indent_save_json('asset packs/' + self.pack + '/images.json',self.image_json)
                self.url = None
                self.url_input = TextInput("", None, width=c.width - 160, empty="url", no_editor=True)
                self.url_valid = False
                self.preview_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
                name = self.name_input.text
                self.suggestion = None
                print(name)
                if name[-1] in {"0","1","2","3","4","5","6","7","8","9"}:
                    if name[-2] != " ":
                        self.suggestion = name[:-2] + str(int(name[-2:])+1)
                    else:
                        self.suggestion = name[:-1] + str(int(name[-1])+1)
                    self.suggestion_button = Button('"'+self.suggestion+'"',width=300)
                self.name_input = TextInput("", None, width=300, empty="name", no_editor=True)

    def load_image_thread(self, url):
        self.url_valid = False
        try:
            response = requests.get(url, timeout=5)
            img = io.BytesIO(response.content)
            img = pygame.image.load(img).convert_alpha()
            self.preview_surf = scale_image(img, 200)
            self.url_valid = True
        except:
            self.url_surf = c.editor_font.render("Invalid URL", True, (255, 150, 150))

