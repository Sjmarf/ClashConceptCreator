import pygame
from scripts import common as c
from scripts.utility.size_element import size_element
from scripts.utility.scale_image import scale_image
from scripts.utility.file_manager import get_file_list

from scripts.editor_objects.small_button import SmallButton
from scripts.editor_objects.text_input import TextInput
from scripts.menus.editor_sub.image_selection import ImageSelection


class TroopEditor:
    def __init__(self):
        self.surf = pygame.Surface((c.width - 100, c.height - 100), pygame.SRCALPHA)
        self.edit_box = size_element('assets/editor_gui/troop_box.png', (300, c.height - 290), (30, 30, 30, 30))
        self.troop_img = pygame.image.load('assets/editor_gui/troop.png').convert_alpha()
        self.new_troop_img = pygame.image.load('assets/editor_gui/troop_add.png').convert_alpha()
        self.data = c.data["el"][c.selected[0]][3]

        self.image_selection = ImageSelection(size=(c.width - 460, c.height - 290))
        self.add_button_x = None
        self.selected = None
        self.need_preview = False
        self.preview_surf = None

        self.bin_button = SmallButton(icon="bin_button")
        self.text1 = TextInput("", None, width=250)
        self.text2 = TextInput("", None, width=250, int_only=True)

        self.draw_troop_list()

    def draw_troop_list(self):
        self.troop_list = size_element('assets/editor_gui/troop_box.png', (c.width - 140, 100), (30, 30, 30, 30))
        x = 20
        for troop in self.data:
            self.troop_list.blit(self.troop_img, (x, 10))
            if troop[0] is not None:
                image_name = troop[0] + ".png"
                if image_name in get_file_list('projects/' + c.project_name + '/images'):
                    img = pygame.image.load('projects/' + c.project_name + '/images/' + image_name)
                    img = scale_image(img, 54)
                    self.troop_list.blit(img, (x+3, 10+23))
            x += 70

        if x < x * 10:
            self.troop_list.blit(self.new_troop_img, (x, 10))
            self.add_button_x = x
        else:
            self.add_button_x = None

    def render(self):
        self.surf.fill((50, 50, 55))
        self.surf.blit(self.troop_list, (20, 50))

        if self.selected is not None:
            self.surf.blit(self.edit_box, (20, 170))
            self.surf.blit(self.title, (160 - self.title.get_width() // 2, 180))
            self.bin_button.render(self.surf, (280, 180))
            self.surf.blit(self.preview_surf, (170 - 50, 220))

            self.text1.render(self.surf, (45, 350))
            self.text2.render(self.surf, (45, 390))

            self.image_selection.render(self.surf, (340, 170), scrollbar_mouse_y_offset=-50)

        c.display.blit(self.surf, (50, 50))

        if self.selected is not None:
            if self.data[self.selected][0] is not None:
                image_name = self.data[self.selected][0] + ".png"
                if image_name in get_file_list('projects/' + c.project_name + '/images'):
                    self.need_preview = False
                    img = pygame.image.load('projects/' + c.project_name + '/images/' + image_name)
                    self.preview_surf = scale_image(img, 100)
                    self.draw_troop_list()

    def switch_selected(self, num):
        self.selected = num
        # Title
        text = self.data[num][0]
        if text is None:
            text = "(Blank)"
        else:
            text = text.split("- ")[1]
        self.title = c.editor_font.render(text, True, (200, 200, 205))
        # Remove selection highlight
        self.image_selection.image_clicked = None
        # Image preview
        self.preview_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        #Text inputs
        self.text1 = TextInput(self.data[num][1], None, width=250)
        self.text2 = TextInput(self.data[num][2], None, width=250, int_only=True)

    def event(self, event):
        pos = (0, 0)
        if event.type == pygame.VIDEORESIZE:
            self.surf = pygame.Surface((c.width - 100, c.height - 100))
            self.image_selection.resize((c.width - 460, c.height - 290))
            self.edit_box = size_element('assets/editor_gui/troop_box.png', (300, c.height - 290), (30, 30, 30, 30))
            self.draw_troop_list()

        if event.type in {pygame.MOUSEBUTTONDOWN, pygame.MOUSEWHEEL}:
            pos = pygame.mouse.get_pos()
            pos = (pos[0] - 50, pos[1] - 50)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Select troop
                x = 40
                for num, troop in enumerate(self.data):
                    rect = pygame.Rect(x, 60, 60, 80)
                    if rect.collidepoint(pos):
                        self.switch_selected(num)
                        self.need_preview = True
                        return
                    x += 70
                if self.add_button_x is not None:
                    # Add button
                    rect = pygame.Rect(20+self.add_button_x, 60, 60, 80)
                    if rect.collidepoint(pos):
                        self.data.append([None, "", ""])
                        self.draw_troop_list()

                if self.selected is not None:
                    if self.bin_button.click(event, pos):
                        del self.data[self.selected]
                        self.selected = None
                        self.draw_troop_list()

        if self.selected is not None:
            output = self.image_selection.event(event, pos)
            if output is not None:
                self.data[self.selected][0] = output[5] + output[0]
                self.title = c.editor_font.render(output[0], True, (200, 200, 205))
                self.preview_surf = scale_image(output[1], 100)
                self.need_preview = True

            if self.text1.event(event, pos):
                self.data[self.selected][1] = self.text1.text
            if self.text2.event(event, pos):
                self.data[self.selected][2] = self.text2.text
