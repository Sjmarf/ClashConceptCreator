import pygame
from scripts import common as c
from scripts.utility.file_manager import getFileList
from scripts.editor_objects.button import Button
from scripts.editor_objects.small_button import SmallButton
from _thread import start_new_thread


class Slider:
    def __init__(self, val):
        self.background = pygame.image.load('assets/editor_gui/text_input.png').convert_alpha()
        self.slider = pygame.image.load('assets/editor_gui/slider.png').convert_alpha()
        self.val, self.picked_up = val, False
        self.pos = (0, 0)

    def render(self, surf, pos, window_pos):
        self.pos = pos
        surf.blit(self.background, pos)
        surf.blit(self.slider, (pos[0] + self.val * 1.35, pos[1]))

        if self.picked_up:
            mouse_x = 0 - window_pos[0] - pos[0] + pygame.mouse.get_pos()[0] - 7
            self.val = min(max(0, mouse_x / 1.35), 100)

    def event(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (pos[0] - self.pos[0], pos[1] - self.pos[1])
            rect = pygame.Rect((self.val * 1.35, 0, 15, 30))
            if rect.collidepoint(pos):
                self.picked_up = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.picked_up = False


class ColourSelection:
    def __init__(self, pos, colour, set_path):
        self.pos, self.set_path = pos, set_path
        self.surf = pygame.Surface((510, 200), pygame.SRCALPHA)
        self.colour_preview = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.colour_obj = pygame.Color(colour)
        self.small_font = pygame.font.SysFont("Monospace", 10)
        self.eyedropper = SmallButton(icon='eyedropper_button')

        hsva = self.colour_obj.hsva
        self.sliders = [Slider(hsva[0] / 3.6), Slider(hsva[1]), Slider(hsva[2])]

        preset_colours = [
            (255, 255, 255),
            (0, 0, 0),
            (132, 204, 44),  # Button green
            (196, 8, 11),  # Button red (actual 208, 12, 15)
            (229, 229, 178),  # Button Cream (chat send button)
            (46, 147, 207),  # Button cyan
            (158, 229, 106),  # Text green
            (214, 209, 146),  # Chat text player name
            (119, 119, 111),  # Chat text player role
            (51, 92, 155),  # Troop description text blue
            (230, 230, 222),  # Box light beige
            (206, 201, 195),  # Box dark beige
            (187, 187, 187),  # Box troop gradient grey
            (66, 66, 62),  # Chat grey
            (92, 92, 79),  # Menu header
            (144, 216, 56),  # Stat bar green
            (31, 7, 44),  # Magic Item background dark purple
        ]
        self.presets = []
        for col in preset_colours:
            surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            surf.fill(col)
            self.presets.append((surf, col))

        self.colour_mode = "HSV"
        self.mode_button = Button("Mode: HSV", width=180)

    def render(self):
        self.surf.fill((50, 50, 55))

        if c.submenu_2_update:
            self.colour_obj.update(c.submenu_2_update_value)
            self.update_slider_pos()

        if self.colour_mode == "HSV":
            self.colour_obj.hsva = (self.sliders[0].val * 3.6, self.sliders[1].val, self.sliders[2].val, 100)
        else:
            self.colour_obj.update((
                self.sliders[0].val * 2.55, self.sliders[1].val * 2.55, self.sliders[2].val * 2.55))

        c.data["el"][self.set_path[0]][self.set_path[1]] = tuple(self.colour_obj)
        self.colour_preview.fill(self.colour_obj)
        self.surf.blit(self.colour_preview, (390, 20))
        hsva = (round(self.colour_obj.hsva[0]), round(self.colour_obj.hsva[1]), round(self.colour_obj.hsva[2]))
        text_surf = self.small_font.render("HSV: " + str(hsva), True, (100, 100, 105))
        self.surf.blit(text_surf, (390, 140))
        text_surf = self.small_font.render("RGB: " + str(self.colour_obj[0:3]), True, (100, 100, 105))
        self.surf.blit(text_surf, (390, 160))

        self.mode_button.render(self.surf, (180, 20))
        y = 60

        for letter, slider in zip(self.colour_mode, self.sliders):
            slider.render(self.surf, (210, y), self.pos)
            text_surf = c.editor_font.render(letter, True, (200, 200, 205))
            self.surf.blit(text_surf, (180, y + 1))
            y += 40

        x, y = 20, 20
        for preset in self.presets:
            self.surf.blit(preset[0], (x, y))
            x += 30
            if x >= 170:
                x = 20
                y += 30

        self.eyedropper.render(self.surf, (10, 160))

        c.display.blit(self.surf, self.pos)

    def update_slider_pos(self):
        if self.colour_mode == "RGB":
            for num, slider in enumerate(self.sliders):
                slider.val = self.colour_obj[num] / 2.55
        else:
            self.sliders[0].val = self.colour_obj.hsva[0] / 3.6
            self.sliders[1].val = self.colour_obj.hsva[1]
            self.sliders[2].val = self.colour_obj.hsva[2]

    def event(self, event):
        m_pos = (0, 0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                c.menu.side_bar.changeMenu()

        if event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = (event.pos[0] - self.pos[0], event.pos[1] - self.pos[1])

            if self.eyedropper.click(event, m_pos):
                from scripts.menus.editor_sub.eyedropper import Eyedropper
                c.submenu2 = Eyedropper()

            if self.mode_button.click(event, m_pos):
                if self.colour_mode == "HSV":
                    self.colour_mode = "RGB"
                else:
                    self.colour_mode = "HSV"
                self.update_slider_pos()
                self.mode_button = Button("Mode: " + self.colour_mode, width=180)

            else:
                x, y = 20, 20
                for preset in self.presets:
                    rect = pygame.Rect(x, y, 20, 20)
                    if rect.collidepoint(m_pos):
                        self.colour_obj.update(preset[1])
                        self.update_slider_pos()
                    x += 30
                    if x >= 170:
                        x = 20
                        y += 30

        for slider in self.sliders:
            slider.event(event, m_pos)
