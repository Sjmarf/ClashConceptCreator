import pygame
from scripts import common as c
from scripts.editor_objects.text_input import TextInput
from scripts.editor_objects.choice_input import ChoiceInput
from scripts.editor_objects.button import Button
from scripts.utility.file_manager import saveJson, loadJson
from scripts.utility import font


class Export:
    def __init__(self):
        self.data = loadJson('data/watermark.json')
        self.surf = pygame.Surface((300, 480), pygame.SRCALPHA)
        self.output_surf = c.canvas.copy()
        self.preview = pygame.transform.smoothscale(c.canvas, (250, 140))

        self.export_button = Button("Export", width=250)
        self.watermark_type = ChoiceInput(self.data["type"], None, ["None", "Bottom-left", "Centre"],
                                          label="Watermark type", mode="buttons", submenu_layer=2, width=250)
        self.watermark_text = TextInput(self.data["text"], None, label="Watermark Text", width=250)
        self.upscale = ChoiceInput(self.data["upscale"], None, ["Off", "2x"],
                                   label="Upscale", mode="buttons", submenu_layer=2, width=250)
        self.watermark_type_name = self.data["type"]
        self.create_watermark_surf()

    def create_watermark_surf(self):
        self.output_surf = c.canvas.copy()
        text = self.watermark_text.text

        if self.watermark_type.text == "Bottom-left":
            text_surf = font.renderText(text, "default", 20)
            self.output_surf.blit(text_surf, (10, 710))
        elif self.watermark_type.text == "Centre":
            text_surf = font.renderText(text, "default", 30)
            text_surf.set_alpha(150)
            self.output_surf.blit(text_surf,
                                  (c.canvas_size[0] / 2 - text_surf.get_width() // 2, c.canvas_size[1] / 2 - text_surf.get_height() // 2))
        self.preview = pygame.transform.smoothscale(self.output_surf, (250, 140))

    def render(self):
        self.surf.fill((50, 50, 55))
        self.surf.blit(self.preview, (25, 25))

        self.watermark_type.render(self.surf, (25, 190))
        self.watermark_type.window_pos_x = c.width // 2 - 130 + 25
        self.watermark_text.render(self.surf, (25, 260))
        self.upscale.render(self.surf, (25, 330))
        self.upscale.window_pos_x = c.width // 2 - 130 + 25
        self.export_button.render(self.surf, (25, 420))

        c.display.blit(self.surf, (c.width // 2 - 130, c.height // 2 - 240))

        self.create_watermark_surf()

    def event(self, event):
        pos = (0, 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - (c.width // 2 - 130), event.pos[1] - (c.height // 2 - 240))

        self.watermark_type.event(event, pos)
        self.upscale.event(event, pos)
        self.watermark_text.event(event, pos)

        if self.export_button.click(event, pos):
            img = self.output_surf
            watermark = pygame.image.load('assets/editor_gui/watermark.png').convert_alpha()
            img.blit(watermark, (2, img.get_height() - 2 - watermark.get_height()))
            proj = c.project_name
            if "/" in proj:
                proj = proj.split("/")[-1]
            path = 'exports/' + proj + '.png'

            if self.upscale.text == "2x":
                img = pygame.transform.smoothscale(img,(c.canvas_size[0]*2,c.canvas_size[1]*2))
            pygame.image.save(img, path)

            import os
            from webbrowser import open as openFileLocation
            openFileLocation('file://' + os.getcwd() + "/exports")
            del openFileLocation, os

            # Save changes
            self.data["type"] = self.watermark_type.text
            self.data["text"] = self.watermark_text.text
            self.data["upscale"] = self.upscale.text
            saveJson('data/watermark.json', self.data)
            c.submenu = None
