import pygame

from scripts import common as c
from scripts.editor_objects.button import Button
from scripts.editor_objects.asset_pack_button import AssetPackButton

from scripts.utility.file_manager import get_file_list, load_json, save_json
from scripts.utility.size_element import size_element
from scripts.utility.text_lines import text_lines

class AssetPacks:
    def __init__(self):
        self.back_button = Button("< Back", width=100)
        self.background = None
        self.page = None
        self.reorder = pygame.image.load('assets/editor_gui/reorder.png').convert_alpha()
        self.plus = pygame.image.load('assets/editor_gui/plus.png').convert_alpha()

        fade = pygame.image.load('assets/editor_gui/gradient_2.png').convert_alpha()
        self.fade = pygame.transform.scale(fade, (30, c.height))
        self.edit_button = Button("Add images", width=200)

        self.title_enabled = c.editor_font.render("Enabled:", True, (150, 255, 150))
        self.title_disabled = c.editor_font.render("Disabled:", True, (255, 150, 150))

        self.enabled_packs = load_json('asset packs/enabled_packs.json')
        self.packs_list = get_file_list('asset packs')
        self.packs_list.remove("enabled_packs.json")
        if ".gitkeep" in self.packs_list:
            self.packs_list.remove(".gitkeep")

        self.reorder_bar = pygame.Surface((260, 2), pygame.SRCALPHA)
        self.reorder_bar.fill((255, 255, 255))
        self.reorder_positions = []

        self.pack_buttons = {}
        for pack in self.packs_list:
            data = load_json('asset packs/' + pack + '/search_data.json')
            self.pack_buttons[pack] = AssetPackButton(pack, data["label_colour"], align="left")

        self.picked_up = None

        self.draw_no_page_surf()

    def draw_no_page_surf(self):
        self.page = None
        self.no_page_surf = pygame.Surface((c.width - 300, c.height))
        self.no_page_surf.fill((30, 30, 35))
        img = pygame.image.load('assets/editor_gui/clans.png').convert_alpha()
        self.no_page_surf.blit(img, (self.no_page_surf.get_width() // 2 - img.get_width() // 2, 60))
        lines = ["Asset Packs are collections of textures for",
                 "you to use in your concepts. You can choose",
                 "which packs you want to enable."]

        y = 250
        for line in lines:
            text_surf = c.editor_font.render(line, True, (170, 170, 255))
            self.no_page_surf.blit(text_surf, (self.no_page_surf.get_width() // 2 - text_surf.get_width() // 2, y))
            y += 40

    def switch_page(self, pack_name):
        self.page = pack_name
        self.background = pygame.Surface((c.width - 300, c.height))
        img = pygame.image.load('asset packs/' + pack_name + '/background.png').convert()
        img = pygame.transform.smoothscale(img, (img.get_width() / img.get_height() * c.height, c.height))
        self.background.blit(img, (self.background.get_width() // 2 - img.get_width() // 2, 0))

        data = load_json('asset packs/' + pack_name + '/data.json')
        self.pack_title = size_element('assets/editor_gui/box.png', (500, 110), (30, 30, 30, 30))
        # Title
        text_surf = c.editor_font.render(data["title"], True, (250, 250, 255))
        self.pack_title.blit(text_surf, (250 - text_surf.get_width() // 2, 7))
        # Subtitle
        text_surf = c.editor_font_small.render(data["subtitle"], True, (150, 150, 155))
        self.pack_title.blit(text_surf, (250 - text_surf.get_width() // 2, 36))
        # Description
        desc_surf = text_lines(data["description"], 460)
        self.pack_desc = size_element('assets/editor_gui/box.png', (500, desc_surf.get_height() + 40), (30, 30, 30, 30))
        self.pack_desc.blit(desc_surf, (20, 20))
        # Get count
        online_images = len(load_json('asset packs/' + pack_name + '/images.json').keys())
        local_images = len(get_file_list('asset packs/' + pack_name + '/local'))
        icons = len(get_file_list('asset packs/' + pack_name + '/icons'))
        buttons = load_json('asset packs/' + pack_name + '/buttons/buttons.json')
        buttons = len(buttons["large"])+len(buttons["small"])
        # Counters
        self.pack_counters = size_element('assets/editor_gui/box.png', (500, 20*4+40), (30, 30, 30, 30))
        text_surf = c.editor_font_small.render('Online images: '+ str(online_images), True, (100, 255, 255))
        self.pack_counters.blit(text_surf, (20, 20))
        text_surf = c.editor_font_small.render('Local Images: ' + str(local_images), True, (100, 255, 255))
        self.pack_counters.blit(text_surf, (20, 40))
        text_surf = c.editor_font_small.render('Icons: ' + str(icons), True, (100, 255, 255))
        self.pack_counters.blit(text_surf, (20, 60))
        text_surf = c.editor_font_small.render('Buttons: ' + str(buttons), True, (100, 255, 255))
        self.pack_counters.blit(text_surf, (20, 80))

    def render(self):
        c.display.fill((50, 50, 55))

        self.back_button.render(c.display, (20, 20))
        self.reorder_positions = []

        # Enabled packs
        c.display.blit(self.title_enabled, (20, 80))

        y = 120
        disabled_packs = list(set(self.packs_list) - set(self.enabled_packs))
        for pack in self.enabled_packs:
            c.display.blit(self.reorder, (10, y))
            alpha = 255
            if self.picked_up == pack:
                self.reorder_positions.append(y - 5)
                alpha = 50
            else:
                self.reorder_positions.append(y - 5)
            self.pack_buttons[pack].render(c.display, (60, y), alpha=alpha)
            y += 40

        self.reorder_positions.append(y - 5)

        # Disabled packs
        y += 20
        c.display.blit(self.title_disabled, (20, y))
        y += 40
        self.reorder_positions.append(y)
        for pack in disabled_packs:
            c.display.blit(self.plus, (10, y))
            self.pack_buttons[pack].render(c.display, (60, y))
            y += 40

        # Reorder bar
        if self.picked_up is not None:
            mouse_y = pygame.mouse.get_pos()[1]
            reorder_y = min(self.reorder_positions, key=lambda m_y: abs(m_y - mouse_y))
            c.display.blit(self.reorder_bar, (20, reorder_y))

        # Page
        if self.page is not None:
            c.display.blit(self.background, (300, 0))
            c.display.blit(self.fade, (300, 0))
            centre = ((c.width - 300) // 2) + 300
            c.display.blit(self.pack_title, (centre - 250, 80))

            self.edit_button.render(c.display, (centre - 100, 145))
            c.display.blit(self.pack_desc, (centre - 250, 200))

            c.display.blit(self.pack_counters, (centre - 250, 210+self.pack_desc.get_height()))

        else:
            c.display.blit(self.no_page_surf, (300, 0))
            c.display.blit(self.fade, (300, 0))

    def event(self, event):
        if event.type == pygame.VIDEORESIZE:
            fade = pygame.image.load('assets/editor_gui/gradient_2.png').convert_alpha()
            self.fade = pygame.transform.scale(fade, (30, c.height))
            if self.page is None:
                self.draw_no_page_surf()
            else:
                self.switch_page(self.page)

        if event.type == pygame.MOUSEBUTTONUP:
            if self.picked_up is not None:
                mouse_y = pygame.mouse.get_pos()[1]
                reorder_y = min(self.reorder_positions, key=lambda m_y: abs(m_y - mouse_y))
                index = self.reorder_positions.index(reorder_y)
                # Disable pack
                if index == len(self.reorder_positions) - 1:
                    if self.picked_up in self.enabled_packs:
                        self.enabled_packs.remove(self.picked_up)
                        save_json('asset packs/enabled_packs.json', self.enabled_packs)
                else:
                    # Move pack
                    old_index = self.enabled_packs.index(self.picked_up)
                    self.enabled_packs[old_index] = self.picked_up+"-REMOVE"
                    self.enabled_packs.insert(max(0,index),(self.picked_up))
                    self.enabled_packs.remove(self.picked_up+"-REMOVE")
                    save_json('asset packs/enabled_packs.json', self.enabled_packs)
                self.picked_up = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.click(event, event.pos):
                from scripts.menus.menus.main_menu import MainMenu
                c.menu = MainMenu(tab=4)

            if event.pos[0] > 60:
                # Pack buttons
                for pack in self.pack_buttons.keys():
                    if self.pack_buttons[pack].click(event, event.pos):
                        self.switch_page(pack)

            else:
                # Pack reorder & add
                y = 120
                disabled_packs = list(set(self.packs_list) - set(self.enabled_packs))

                for pack in self.enabled_packs:
                    rect = pygame.Rect((10, y, 30, 30))
                    if rect.collidepoint(event.pos):
                        self.picked_up = pack
                    y += 40
                y += 60

                for pack in disabled_packs:
                    rect = pygame.Rect((10, y, 30, 30))
                    if rect.collidepoint(event.pos):
                        self.enabled_packs.append(pack)
                        save_json('asset packs/enabled_packs.json', self.enabled_packs)
                    y += 40

            if self.page is not None:
                if self.edit_button.click(event, event.pos):
                    from scripts.menus.menus.new_asset_pack_entry import NewAssetPackEntry
                    c.menu = NewAssetPackEntry(self.page)
