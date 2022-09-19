from scripts import common as c
from scripts.utility.file_manager import load_json, get_file_list
from scripts.utility.scale_image import scale_image
from scripts.utility.size_element import size_element
from scripts.editor_objects.button import Button
from scripts.editor_objects.asset_pack_button import AssetPackButton
from scripts.editor_objects.text_input import TextInput
from scripts.editor_objects.small_button import SmallButton
from scripts.menus.right_click import RightClick
from scripts.editor_objects.scrollbar import Scrollbar
from _thread import start_new_thread
import pygame
import requests
import io
from time import time as current_time


class ImageWindow:
    def __init__(self, path):
        self.path = path
        self.surf = pygame.Surface((c.width - 100, c.height - 100), pygame.SRCALPHA)
        self.image_selection = ImageSelection(size=(c.width - 425, c.height - 150))

        image_name = c.data["el"][self.path[0]][self.path[1]]
        if image_name is not None:
            if image_name + ".png" in get_file_list('projects/' + c.project_name + '/images'):
                img = pygame.image.load('projects/' + c.project_name + '/images/' + image_name + ".png")
                self.preview_img = scale_image(img, 250)
            else:
                self.preview_img = pygame.Surface((250, 250), pygame.SRCALPHA)
        else:
            self.preview_img = pygame.Surface((250, 250), pygame.SRCALPHA)

        self.image_name = image_name
        self.asset_pack_button = None
        self.image_pack = None
        self.need_preview = False
        self.done_button = Button("Done", width=150)

        self.edit_button = Button("edit", width=180)
        self.delete_button = SmallButton(icon="bin_button")

    def render(self):
        self.surf.fill((50, 50, 55))
        self.surf.blit(self.preview_img, (25, 25))
        self.image_selection.render(self.surf, (300, 25), scrollbar_mouse_y_offset=-50)
        self.done_button.render(self.surf, (75, c.height - 155))

        if self.image_name is not None:
            name = self.image_name.title()
            name = name.split("- ")[1]  # Remove asset-pack abbreviation
            if len(name) > 20 and " " in name:
                # Render file name
                # Render on two lines if too long
                words = name.split(" ")
                half = len(words) // 2
                text_surf = c.editor_font.render(" ".join(words[:half]), True, (200, 200, 205))
                self.surf.blit(text_surf, (150 - text_surf.get_width() // 2, 300))
                text_surf = c.editor_font.render(" ".join(words[half:]), True, (200, 200, 205))
                self.surf.blit(text_surf, (150 - text_surf.get_width() // 2, 330))
                asset_pack_y_offset = 30

            else:
                text_surf = c.editor_font.render(name, True, (200, 200, 205))
                self.surf.blit(text_surf, (150 - text_surf.get_width() // 2, 300))
                asset_pack_y_offset = 0

            if self.image_pack is not None:
                # Asset Pack Label
                if self.image_pack == "Local":
                    col = (155, 242, 114)
                elif self.image_pack == "Clan Badge":
                    col = (133, 114, 242)
                else:
                    asset_pack_data = load_json('asset packs/' + self.image_pack + '/search_data.json')
                    col = asset_pack_data["label_colour"]

                if self.asset_pack_button is None:
                    self.asset_pack_button = AssetPackButton(self.image_pack, col)
                if self.asset_pack_button.name != self.image_pack:
                    self.asset_pack_button = AssetPackButton(self.image_pack, col)
                self.asset_pack_button.render(self.surf, (40, 340 + asset_pack_y_offset))

            if self.image_pack == "Clan Badge":
                # Clan Badge Edit & Delete buttons
                self.edit_button.render(self.surf,(40,380+asset_pack_y_offset))
                self.delete_button.render(self.surf, (230, 380 + asset_pack_y_offset))

        c.display.blit(self.surf, (50, 50))

        if self.need_preview:
            if self.image_name + ".png" in get_file_list('projects/' + c.project_name + '/images'):
                img = pygame.image.load('projects/' + c.project_name + '/images/' + self.image_name + ".png")
                self.preview_img = scale_image(img, 250)
                self.need_preview = False

    def event(self, event):
        pos = (0, 0)
        if event.type == pygame.VIDEORESIZE:
            self.surf = pygame.Surface((c.width - 100, c.height - 100), pygame.SRCALPHA)
            self.image_selection.resize((c.width - 425, c.height - 150))

        if event.type in {pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL}:
            pos = pygame.mouse.get_pos()
            pos = (pos[0] - 50, pos[1] - 50)

        output = self.image_selection.event(event, pos)
        # Load low-res preview image
        if output is not None:
            self.image_name, self.image_pack = output[5] + output[0], output[3]
            self.preview_img = scale_image(output[1], 250)
            self.need_preview = True

        if self.done_button.click(event, pos):
            c.data["el"][self.path[0]][self.path[1]] = self.image_name
            c.menu.canvas.draw()
            c.submenu = None

        if self.image_pack == "Clan Badge":
            # Delete Clan Badge design
            if self.delete_button.click(event,pos):
                # Remove preview image
                self.need_preview = False
                self.preview_img = pygame.Surface((250, 250), pygame.SRCALPHA)
                # Remove files for badge
                from os import remove
                name = self.image_name.split("- ")[1]
                remove('assets/clan_badges/' + name + '.png')
                remove('assets/clan_badges/' + name + '.json')
                # Deselect image
                self.image_name = None
                # Reload image search
                self.image_selection.search_num += 1
                self.image_selection.load_images(self.image_selection.search_num)

            # Edit Clan Badge Design
            if self.edit_button.click(event,pos):
                name = self.image_name.split("- ")[1]
                from scripts.menus.editor_sub.badge_creator import BadgeCreator
                c.submenu = BadgeCreator(in_editor=True,menu_to_return_to=c.submenu,file_name=name)

###################################################################################

class ImageSelection:
    def __init__(self, size=(200, 200), no_editor=False):
        self.current_image_data = None
        self.surf = pygame.Surface(size, pygame.SRCALPHA)
        self.surf.fill((45, 45, 50))
        self.pos, self.per_row, self.start_x = (0, 0), 5, 10
        self.size, self.no_editor = size, no_editor
        self.images = []

        self.search_bar = TextInput("", None, width=size[0] - 80, empty="Search...", no_editor=no_editor)
        self.more_button = SmallButton(icon="more_button")
        self.scrollbar = Scrollbar()
        self.right_click = None

        self.search_term = ""
        self.extensions = {".png", ".PNG", ".jpg", ".jpeg"}
        self.loading_text = c.editor_font.render("Loading...", True, (150, 150, 155))
        self.connection_error = False
        self.loading = False
        self.search_num = 0
        self.outline_img = pygame.Surface((56, 56), pygame.SRCALPHA)
        self.image_clicked = None
        pygame.draw.rect(self.outline_img, (255, 255, 255), (0, 0, 56, 56), 3)

        self.no_results_text = c.editor_font.render("We couldn't find any results.", True, (200, 200, 205))
        self.connection_error_text = c.editor_font.render("Connection error.", True, (255, 150, 150))
        self.no_results_img = pygame.image.load("assets/editor_gui/villager_think.png").convert_alpha()
        self.no_results_img = pygame.transform.smoothscale(self.no_results_img, (57, 84))

    def load_from_json(self, num, search_words, pack_name, prefix, suffix, ignore_if_already_extension):
        start = current_time()
        data = load_json('asset packs/' + pack_name + '/images.json')
        keys = data.keys()
        keys = list(filter(lambda x: all(search in x.lower() for search in search_words), keys))
        print("JSON load time:" + str(round(current_time() - start, 4)))
        for name in keys:
            if type(data[name]) != str:
                size, url = data[name][1:], data[name][0]
            else:
                size, url = (0, 0, 400), data[name]
            if (not any(ext in url for ext in self.extensions)) or not ignore_if_already_extension:
                url += suffix
            url = prefix + url
            try:
                response = requests.get(url, timeout=5)
            except requests.exceptions.ConnectionError:
                print("Image load ConnectionError")
                self.connection_error = True
                return None
            img = io.BytesIO(response.content)
            img = pygame.image.load(img).convert_alpha()
            img = scale_image(img, size[2] / 8)
            new_surf = pygame.Surface((50, 50), pygame.SRCALPHA)
            if num != self.search_num:
                # Stops previous search threads when a new one is created
                return True
            new_surf.blit(img,
                          (25 - img.get_width() // 2 + size[0] // 8, 50 - img.get_height() + size[1] // 8))
            # filename, surface, url, pack name, is local
            fancy_name = name.title()
            self.images.append([fancy_name, new_surf, data[name], pack_name, "online"])

        return None

    def load_from_path(self, search_words, path, pack_name, mode="local"):
        local = get_file_list(path)
        local = list(filter(lambda x: all(search in x.lower() for search in search_words), local))
        for name in local:
            if ".png" in name:
                img = pygame.image.load(path + "/" + name).convert_alpha()
                img = scale_image(img, 50)
                name = name.replace(".png", "")
                # filename, surface, url, pack name, is local
                self.images.append([name, img, None, pack_name, mode])

    def load_images(self, num):
        self.connection_error = False
        self.scrollbar.scroll = 0
        self.loading = True

        self.images = []
        search_term = self.search_term.lower()
        search_words = search_term.split(" ")

        # Get list of enabled asset packs
        enabled_packs = load_json('asset packs/enabled_packs.json')

        # Load images from local
        self.load_from_path(search_words, 'local images', "Local")
        self.load_from_path(search_words, 'assets/clan_badges', "Clan Badge")
        # Load images from URL

        for pack in enabled_packs:
            if pack != ".gitkeep":
                self.load_from_path(search_words, 'asset packs/' + pack + '/local', pack)
                self.load_from_path(search_words, 'asset packs/' + pack + '/icons', pack, mode="icon")
                if not self.connection_error:
                    data = load_json('asset packs/' + pack + '/search_data.json')
                    output = self.load_from_json(num, search_words, pack,
                                                 data["prefix"], data["suffix"], data["remove_suffix_if_provided"])
                    if output:
                        print('Killed previous thread')
                        return None

        if num == self.search_num:
            self.loading = False

    def resize(self, size):
        self.scrollbar.scroll = 0
        self.size = size
        self.surf = pygame.Surface(size, pygame.SRCALPHA)
        self.surf.fill((45, 45, 50))
        self.search_bar = TextInput(self.search_bar.text, None, width=size[0] - 80,
                                    empty="Search...", no_editor=self.no_editor)

    def render(self, surf, pos, scrollbar_mouse_y_offset=0):
        self.pos = pos
        self.surf.fill((45, 45, 50))

        self.search_bar.render(self.surf, (20, 20))
        self.more_button.render(self.surf, (self.size[0] - 50, 20))

        self.per_row = (self.size[0] - 50) // 60
        self.start_x = (self.size[0] - self.per_row * 60) // 2

        x, y = self.start_x, 5 - self.scrollbar.scroll

        if len(self.images) == 0:
            if self.search_num != 0 and not self.loading:
                self.surf.blit(self.no_results_img, (self.size[0] // 2 - 172, 100))
                self.surf.blit(self.no_results_text, (self.size[0] // 2 - 105, 120))
            max_scroll = 0
        else:
            max_scroll = 0
            icon_surf = pygame.Surface((self.surf.get_width(), self.surf.get_height() - 55), pygame.SRCALPHA)
            for data in self.images:
                if data[1] is self.image_clicked:
                    icon_surf.blit(self.outline_img, (x - 3, y - 3))
                icon_surf.blit(data[1], (x, y))
                x += 60
                if x / 60 > self.per_row:
                    x = self.start_x
                    y += 60
                    max_scroll += 60
            self.surf.blit(icon_surf, (0, 55))

        self.scrollbar.set_height(self.size[1] - 65, max_scroll)

        self.scrollbar.render(self.surf, (self.size[0] - 30, 55),
                              mouse_y_offset=self.pos[1] * -1 + scrollbar_mouse_y_offset)

        if self.loading:
            self.surf.blit(self.loading_text, (self.size[0] - self.loading_text.get_width() - 40,
                                               self.size[1] - self.loading_text.get_height() - 10))
        if self.connection_error:
            self.surf.blit(self.connection_error_text, (10,
                                                        self.size[1] - self.connection_error_text.get_height() - 10))

        if self.right_click is not None:
            self.right_click.render(self.surf, (self.size[0] - 50 - 190, 60))

        surf.blit(self.surf, pos)

    def load_final_image(self, data, keep_actual_size=False):
        self.current_image_data = data
        name = data[0]
        if data[4] != "online":
            if data[3] == "Local":
                img = pygame.image.load('local images/' + name + ".png")
                filename_prefix = "LOC- "
            elif data[3] == "Clan Badge":
                img = pygame.image.load('assets/clan_badges/' + name + ".png")
                filename_prefix = "CB- "
            else:
                asset_pack_data = load_json('asset packs/' + data[3] + '/search_data.json')
                filename_prefix = asset_pack_data["abbreviation"] + "- "
                if data[4] == "local":
                    folder_name = "local"
                else:
                    folder_name = "icons"
                img = pygame.image.load('asset packs/' + data[3] + '/'+folder_name+'/' + name + ".png")
        else:
            asset_pack_data = load_json('asset packs/' + data[3] + '/search_data.json')
            if type(data[2]) != str:
                size, url = data[2][1:], data[2][0]
            else:
                size, url = (0, 0, 500), data[2]
                keep_actual_size = True
            if (not any(ext in url for ext in self.extensions)) or not asset_pack_data["remove_suffix_if_provided"]:
                url += asset_pack_data["suffix"]
            url = asset_pack_data["prefix"] + url
            response = requests.get(url)
            img = io.BytesIO(response.content)
            img = pygame.image.load(img).convert_alpha()
            if not keep_actual_size:
                img = scale_image(img, size[2])
                new_surf = pygame.Surface((500, 500), pygame.SRCALPHA)
                new_surf.blit(img, (250 - img.get_width() // 2 + size[0], 500 - img.get_height() + size[1]))
                img = new_surf
            filename_prefix = asset_pack_data["abbreviation"] + "- "

        if not self.no_editor:
            pygame.image.save(img, 'projects/' + c.project_name + '/images/' + filename_prefix + name + '.png')
        else:
            data = data.copy()
            data[1] = img
            return data

    def event(self, event, pos):
        pos = (pos[0] - self.pos[0], pos[1] - self.pos[1])
        # Right-click object
        if self.right_click is not None:
            output = self.right_click.event(event, pos)
            if output is not None:
                if output == "Create Clan Badge":
                    from scripts.menus.editor_sub.badge_creator import BadgeCreator
                    if self.no_editor:
                        c.menu.content = BadgeCreator(in_editor=False)
                    else:
                        self.right_click = None
                        c.submenu = BadgeCreator(in_editor=True, menu_to_return_to=c.submenu)

        # Search Bar
        if self.search_bar.event(event, pos):
            if self.search_term != self.search_bar.text:
                self.search_term = self.search_bar.text
                if len(self.search_term) > 2:
                    self.search_num += 1
                    self.loading = True
                    start_new_thread(self.load_images, (self.search_num,))

        # More Button
        if self.more_button.click(event, pos):
            if self.right_click is None:
                self.right_click = RightClick()
                self.right_click.set_options(["Create Clan Badge"], width=220)
            else:
                self.right_click = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Search bar

                rect = pygame.Rect(0, 60, self.size[0], self.size[1] - 60)
                if rect.collidepoint(pos):

                    x, y = self.start_x, 60 - self.scrollbar.scroll
                    for data in self.images:
                        rect = pygame.Rect(x, y, 50, 50)
                        if rect.collidepoint(pos):
                            self.image_clicked = data[1]
                            if not self.no_editor:
                                start_new_thread(self.load_final_image, (data, True))

                            data = data.copy()
                            if data[3] == "Local":
                                data.append("LOC- ")
                            elif data[3] == "Clan Badge":
                                data.append("CB- ")
                            else:
                                asset_pack_data = load_json('asset packs/' + data[3] + '/search_data.json')
                                data.append(asset_pack_data["abbreviation"] + "- ")
                            return data
                        x += 60
                        if x / 60 > self.per_row:
                            x = self.start_x
                            y += 60

        self.scrollbar.event(event, pos, scroll_rect=pygame.Rect(0, 0, self.size[0], self.size[1]))
