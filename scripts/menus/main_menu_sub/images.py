from scripts import common as c
import pygame

from scripts.menus.editor_sub.image_selection import ImageSelection
from _thread import start_new_thread
from scripts.editor_objects.button import Button
from scripts.utility.scale_image import scale_image
from scripts.utility.file_manager import loadJson


class Images:
    def __init__(self):
        self.title = c.editor_font_large.render("Images", True, (250, 250, 255))
        self.subtitle = c.editor_font.render("Search and download assets for your projects.", True, (150, 150, 155))
        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)
        self.image_selection = ImageSelection(size=(c.width - 300, c.height - 300), no_editor=True)
        self.preview = pygame.Surface((150, 150), pygame.SRCALPHA)
        self.image_data = None
        self.is_local = False

        self.download_button = Button("Download full size", width=250)
        self.download_button2 = Button("Download resized", width=250)
        self.open_button = Button("Open in browser", width=250)

    def render(self):
        centre = c.width // 2 - 125
        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)
        self.surf.blit(self.title, (centre - self.title.get_width() // 2, 15))
        self.surf.blit(self.subtitle, (centre - self.subtitle.get_width() // 2, 60))

        self.surf.blit(self.preview, (centre - 207, 100))
        if self.image_data is not None:
            self.download_button.render(self.surf, (centre - 42, 120))
            self.download_button2.render(self.surf, (centre - 42, 160))
            if not self.image_data[4]:
                self.open_button.render(self.surf, (centre - 42, 200))

        self.image_selection.render(self.surf, (25, 275))

        c.display.blit(self.surf, (250, 0))

    def event(self, event, pos):
        if event.type == pygame.VIDEORESIZE:
            self.image_selection.resize(size=(c.width - 300, c.height - 300))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.download_button.click(event,pos):
                self.download_image(keep_actual_size=True)
            elif self.download_button2.click(event,pos):
                self.download_image()

            elif self.open_button.click(event,pos):
                if not self.image_data[4]:
                    asset_pack_data = loadJson('asset packs/' + self.image_data[3] + '/search_data.json')
                    from webbrowser import open
                    url = self.image_data[2]
                    if type(url) == list:
                        url = url[0]
                    url = asset_pack_data["prefix"] + url
                    extensions = {".png", ".PNG", ".jpg", ".jpeg"}
                    if (not any(ext in url for ext in extensions)) or not asset_pack_data["remove_suffix_if_provided"]:
                        url += asset_pack_data["suffix"]
                    open(url)

        output = self.image_selection.event(event, pos)
        if output is not None:
            start_new_thread(self.load_image, (output,))

    def load_image(self, data):
        image = self.image_selection.load_final_image(data)
        self.image_data = image
        self.preview = scale_image(image[1],150)

    def download_image(self, keep_actual_size=False):
        image = self.image_selection.load_final_image(self.image_data,keep_actual_size=keep_actual_size)
        pygame.image.save(image[1], 'exports/' + image[5] + self.image_data[0] + '.png')
        import os
        from webbrowser import open as openFileLocation
        openFileLocation('file://' + os.getcwd() + "/exports")
        del openFileLocation, os
