from scripts import common as c
import pygame

from scripts.menus.editor_sub.image_selection import ImageSelection
from _thread import start_new_thread
from scripts.editor_objects.button import Button
from scripts.editor_objects.small_button import SmallButton
from scripts.editor_objects.asset_pack_button import AssetPackButton
from scripts.utility.scale_image import scale_image
from scripts.utility.file_manager import load_json


class Images:
    def __init__(self):
        self.title = c.editor_font_large.render("Images", True, (250, 250, 255))
        self.subtitle = c.editor_font.render("Search and download assets for your projects.", True, (150, 150, 155))
        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)
        self.image_selection = ImageSelection(size=(c.width - 300, c.height - 300), no_editor=True)
        self.preview = pygame.Surface((150, 150), pygame.SRCALPHA)
        self.image_data = None
        self.is_local = False

        self.download_button = Button("Download full size", width=220)
        self.download_button2 = Button("Download resized", width=220)
        self.open_button = Button("Open in browser", width=220)
        self.edit_button = Button("Edit",width=180)
        self.delete_button = SmallButton(icon="bin_button")

    def render(self):
        centre = c.width // 2 - 125
        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)
        self.surf.blit(self.title, (centre - self.title.get_width() // 2, 15))
        self.surf.blit(self.subtitle, (centre - self.subtitle.get_width() // 2, 60))

        if self.image_data is not None:
            # Left side
            if c.width > 930:
                self.surf.blit(self.image_title, (centre-210-self.image_title.get_width()//2,130))
                self.asset_pack.render(self.surf, (centre-320,170))
                if self.image_data[3] == "Clan Badge":
                    self.edit_button.render(self.surf, (centre-320,210))
                    self.delete_button.render(self.surf, (centre - 130, 210))
            else:
                centre -= 110

            # Image preview
            self.surf.blit(self.preview, (centre - 75, 110))

            # Right side
            self.download_button.render(self.surf, (centre + 100, 130))
            self.download_button2.render(self.surf, (centre + 100, 170))
            if self.image_data[4] == "online":
                self.open_button.render(self.surf, (centre + 100, 210))

        # Image selection box
        self.image_selection.render(self.surf, (25, 275))

        c.display.blit(self.surf, (250, 0))

    def event(self, event, pos):
        if event.type == pygame.VIDEORESIZE:
            self.image_selection.resize(size=(c.width - 300, c.height - 300))

        if self.image_data is not None and c.width > 930:
            if self.image_data[3] == "Clan Badge":
                # Delete Clan Badge design
                if self.delete_button.click(event,pos):
                    from os import remove
                    remove('assets/clan_badges/' + self.image_data[0] + '.png')
                    remove('assets/clan_badges/' + self.image_data[0] + '.json')
                    # Deselect image
                    self.image_data = None
                    # Reload image search
                    self.image_selection.search_num += 1
                    self.image_selection.load_images(self.image_selection.search_num)

                # Edit Clan Badge design
                if self.edit_button.click(event,pos):
                    from scripts.menus.editor_sub.badge_creator import BadgeCreator
                    c.menu.content = BadgeCreator(in_editor=False, file_name=self.image_data[0])

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.download_button.click(event,pos):
                self.download_image(keep_actual_size=True)
            elif self.download_button2.click(event,pos):
                self.download_image()

            elif self.open_button.click(event,pos):
                if not self.image_data[4]:
                    asset_pack_data = load_json('asset packs/' + self.image_data[3] + '/search_data.json')
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
            self.preview = scale_image(output[1],150)
            # Create title
            if c.editor_font.size(output[0])[0] > 220:
                words = output[0].split(" ")
                num = -2
                while True:
                    title = " ".join(words[:num])+"... "+words[-1]
                    if c.editor_font.size(title)[0] < 220:
                        self.image_title = c.editor_font.render(title, True, (200,200,205))
                        break
                    num -= 1
                    if num < len(words)*-1:  # This is a failsafe, it isn't actually needed
                        print('title crop-down error')
                        self.image_title = c.editor_font.render('ERROR', True, (200, 200, 205))
                        break
            else:
                self.image_title = c.editor_font.render(output[0], True, (200, 200, 205))

            self.asset_pack = AssetPackButton(output[3])
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
