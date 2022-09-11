from scripts import common as c
import pygame

from scripts.editor_objects.button import Button
from scripts.editor_objects.colour_input import ColourInput
from scripts.editor_objects.text_input import TextInput
from scripts.utility.font import renderText
from scripts.utility.file_manager import get_file_list, save_json, load_json
from scripts.utility.scale_image import scale_image
from scripts.utility.size_element import size_element
from _thread import start_new_thread


class BadgeCreator:
    def __init__(self, in_editor=False, menu_to_return_to=None, file_name=None):
        self.in_editor, self.menu_to_return_to = in_editor, menu_to_return_to
        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)
        self.preview = pygame.Surface((160, 160), pygame.SRCALPHA)

        self.back_button = Button("< Back", width=100)
        self.save_button = Button("Save",width=100)
        self.save_as_new_button = Button("Save as New", width=160)

        self.file_name = file_name
        if file_name is None:
            self.title = c.editor_font.render("Create Clan Badge", True, (250, 250, 255))
            self.data = {
                "version": c.settings["version"],
                "background_col": (225, 213, 209),
                "foreground_col": (178, 57, 58),
                "foreground_name": "pattern01",
                "border_name": "border1",
                "level": "1"}
        else:
            self.title = c.editor_font.render("Edit Clan Badge", True, (250, 250, 255))
            self.data = load_json('assets/clan_badges/'+file_name+'.json')

        self.level_input = TextInput(self.data["level"],None,label="Level",int_only=True,no_editor=True)


        self.submenu = None
        self.colour_editing = None
        self.create_pattern_list_surf()
        self.create_border_list_surf()
        self.create_preview_surf()
        self.create_colour_inputs()

    def create_colour_inputs(self):
        bg_presets = (
            (157, 61, 65),  # Red
            (225, 213, 209),  # Cream
            (55, 53, 92),  # Navy Blue
            (213, 191, 87),  # Yellow
            (166, 111, 173),  # Pink
            (44, 46, 45),  # Black
            (94, 61, 124),  # Purple
            (64, 116, 169),  # Blue
            (202, 99, 75),  # Orange
            (89, 151, 89),  # Green
            (96, 148, 192),  # Light blue
            (64, 93, 155),  # Dark blue
            (240, 240, 240),  # White
        )
        fg_presets = (
            (178, 57, 58),  # Red
            (249, 238, 231),  # Cream
            (251, 236, 90),  # Yellow
            (50, 54, 55),  # Black
            (136, 62, 130),  # Purple
            (41, 112, 169),  # Blue
            (241, 97, 66),  # Orange
            (64, 156, 85),  # Green
            (0, 72, 128),  # Dark blue
        )
        if self.in_editor:
            self.bg_col = ColourInput(self.data["background_col"], None, label="Background",
                                      submenu_target=2,presets_list=bg_presets)
            self.fg_col = ColourInput(self.data["foreground_col"], None, label="Foreground",
                                      submenu_target=2,presets_list=fg_presets)
        else:
            self.bg_col = ColourInput(self.data["background_col"], None, label="Background",
                                      submenu_target="main_menu", presets_list=bg_presets)
            self.fg_col = ColourInput(self.data["foreground_col"], None, label="Foreground",
                                      submenu_target="main_menu", presets_list=fg_presets)

    def create_preview_surf(self):
        # Frame
        self.preview = pygame.image.load(
            'assets/elements/clan badge/border/'+self.data["border_name"]+'.png').convert_alpha()
        # Background
        bg = pygame.image.load('assets/elements/clan badge/background.png').convert_alpha()
        bg.fill(self.data["background_col"], special_flags=pygame.BLEND_RGB_ADD)
        self.preview.blit(bg, (0, 0))
        # Foreground
        fg = pygame.image.load('assets/elements/clan badge/pattern/'
                               + self.data["foreground_name"] + ".png").convert_alpha()
        if self.data["foreground_name"] != "rainbow":
            fg.fill(self.data["foreground_col"], special_flags=pygame.BLEND_RGB_ADD)
        self.preview.blit(fg, (0, 0))
        # Level
        if self.data["level"] != "":
            level_bg = pygame.image.load(
                'assets/elements/clan badge/level/'+self.data["border_name"]+'.png').convert_alpha()
            self.preview.blit(level_bg,(0,0))
            text_surf = renderText(self.data["level"],"custom",25,font_type="small",col=(255,255,255))
            self.preview.blit(text_surf,(80-text_surf.get_width()//2,15))

    def create_pattern_list_surf(self):
        if self.in_editor:
            self.pattern_surf = pygame.Surface((c.width - 100, 300), pygame.SRCALPHA)
        else:
            self.pattern_surf = pygame.Surface((c.width - 250, 300), pygame.SRCALPHA)
        self.patterns_list = sorted(get_file_list('assets/elements/clan badge/pattern'))
        pattern_bg = size_element('assets/editor_gui/box2.png', (self.pattern_surf.get_width() - 40, 150),
                                  (30, 30, 30, 30))
        self.pattern_surf.blit(pattern_bg, (20, 0))
        x, y = 40, 20
        for pattern in self.patterns_list:
            img = pygame.image.load('assets/elements/clan badge/pattern/' + pattern)
            img = scale_image(img, 40)
            if pattern != "rainbow.png":
                if self.data["foreground_name"] + ".png" == pattern:
                    col = (255, 255, 255)
                else:
                    col = self.data["foreground_col"]
                img.fill(col, special_flags=pygame.BLEND_RGB_ADD)
            self.pattern_surf.blit(img, (x, y))
            x += 40
            if x > self.pattern_surf.get_width() - 70:
                x = 40
                y += 40

    def create_border_list_surf(self):
        if self.in_editor:
            self.border_surf = pygame.Surface((c.width - 100, 300), pygame.SRCALPHA)
        else:
            self.border_surf = pygame.Surface((c.width - 250, 300), pygame.SRCALPHA)
        self.borders_list = sorted(get_file_list('assets/elements/clan badge/border'))
        border_bg = size_element('assets/editor_gui/box2.png', (self.pattern_surf.get_width() - 40, 80),
                                  (30, 30, 30, 30))
        self.border_surf.blit(border_bg, (20, 0))
        x, y = 40, 20
        for border in self.borders_list:
            img = pygame.image.load('assets/elements/clan badge/border/' + border)
            img = scale_image(img, 40)
            self.border_surf.blit(img, (x, y))
            x += 40
            if x > self.border_surf.get_width() - 70:
                x = 40
                y += 40

    def render(self, surf=None):

        centre = c.width // 2 - 125
        if self.in_editor:
            width = c.width - 100
            self.surf = pygame.Surface((c.width - 100, c.height - 100), pygame.SRCALPHA)
            self.surf.fill((50, 50, 55))
        else:
            width = c.width - 250
            self.surf = pygame.Surface((width, c.height), pygame.SRCALPHA)

        # Title
        # Don't render if the title overlaps the save buttons
        if self.file_name is None or centre + self.title.get_width() // 2 < width - 300:
            self.surf.blit(self.title, (centre - self.title.get_width() // 2, 20))

        # Buttons
        self.back_button.render(self.surf, (20, 20))
        if self.file_name is None:
            self.save_as_new_button.render(self.surf, (width-170,20))
        else:
            self.save_button.render(self.surf, (width-120,20))
            self.save_as_new_button.render(self.surf, (width - 290, 20))

        # Surfaces
        self.surf.blit(self.preview, (centre - 80, 70))
        self.surf.blit(self.pattern_surf, (0, 230))
        self.surf.blit(self.border_surf, (0, 400))

        # Colour pickers and Level Input
        self.bg_col.render(self.surf, (width - 200, 70))
        self.fg_col.render(self.surf, (width - 200, 150))
        self.level_input.render(self.surf, (50, 150))

        if self.submenu is not None:
            if self.in_editor:
                dark_surf = pygame.Surface((c.width - 100, c.height - 100), pygame.SRCALPHA)
            else:
                dark_surf = pygame.Surface((width, c.height), pygame.SRCALPHA)
            dark_surf.fill((0, 0, 0, 100))
            self.surf.blit(dark_surf, (0, 0))

        if self.in_editor:
            c.display.blit(self.surf, (50, 50))
        else:
            c.display.blit(self.surf, (250, 0))

        if self.submenu is not None:
            self.submenu.render()

        if self.in_editor:
            if c.submenu_2_update:
                self.get_colour()

    def get_colour(self):
        if self.in_editor:
            col = tuple(c.submenu_2_update_value)
        else:
            col = tuple(self.submenu.colour_obj)
        if self.colour_editing == "background":
            self.data["background_col"] = col
        else:
            self.data["foreground_col"] = col
        self.create_colour_inputs()
        self.create_pattern_list_surf()
        self.create_preview_surf()
        self.submenu = None

    def save(self):
        pygame.image.save(self.preview, 'assets/clan_badges/' + self.file_name + '.png')
        save_json('assets/clan_badges/' + self.file_name + '.json', self.data)
        print("Saved clan badge")

    def event(self, event, pos=(0, 0)):

        if event.type == pygame.MOUSEBUTTONDOWN and self.in_editor:
            pos = (event.pos[0] - 50, event.pos[1] - 50)

        if event.type == pygame.VIDEORESIZE:
            self.create_pattern_list_surf()
            self.create_border_list_surf()

        if self.submenu is not None:
            self.submenu.event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.get_colour()

        else:
            if self.level_input.event(event,pos):
                self.data["level"] = self.level_input.text
                self.create_preview_surf()

            if self.bg_col.event(event, pos):
                self.colour_editing = "background"
                return
            if self.fg_col.event(event, pos):
                self.colour_editing = "foreground"
                return

            if self.back_button.click(event, pos):
                if self.in_editor:
                    data = self.menu_to_return_to.image_selection.current_image_data
                    # Remove old clan badge image
                    if data is not None:
                        name = 'CB- '+data[0]+'.png'
                        if name in get_file_list('projects/'+c.project_name+'/images'):
                            from os import remove
                            remove('projects/'+c.project_name+'/images/'+name)
                            pygame.image.save(self.preview,'projects/'+c.project_name+'/images/'+name)
                    # Update previous menu to reflect changes
                    self.menu_to_return_to.image_selection.search_num += 1
                    start_new_thread(self.menu_to_return_to.image_selection.load_images,(
                        self.menu_to_return_to.image_selection.search_num,))
                    if data is not None:
                        data[1] = self.preview
                        self.menu_to_return_to.image_selection.load_final_image(data)
                    self.menu_to_return_to.need_preview = True
                    # Clear ImageStore
                    c.image_store.element_images = {}
                    c.submenu = self.menu_to_return_to
                else:
                    from scripts.menus.main_menu_sub.images import Images
                    c.menu.content = Images()

            if self.save_as_new_button.click(event, pos):
                file_list = get_file_list('assets/clan_badges')
                num = len(file_list)//2+1
                while "clan badge "+str(num)+".png" in file_list:
                    print("Name already taken, picking another...")
                    num += 1
                self.file_name = 'clan badge '+str(num)
                self.save()

            if self.file_name is not None:
                if self.save_button.click(event,pos):
                    self.save()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = 40, 250
                for pattern in self.patterns_list:
                    rect = pygame.Rect(x,y,40,40)
                    if rect.collidepoint(pos):
                        self.data["foreground_name"] = pattern.replace(".png","")
                        self.create_pattern_list_surf()
                        self.create_preview_surf()
                        return
                    x += 40
                    if x > self.pattern_surf.get_width() - 70:
                        x = 40
                        y += 40

                x, y = 40, 420
                for border in self.borders_list:
                    rect = pygame.Rect(x, y, 40, 40)
                    if rect.collidepoint(pos):
                        self.data["border_name"] = border.replace(".png", "")
                        self.create_border_list_surf()
                        self.create_preview_surf()
                        return
                    x += 40
                    if x > self.border_surf.get_width() - 70:
                        x = 40
                        y += 40
