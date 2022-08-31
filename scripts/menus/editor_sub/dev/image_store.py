import pygame
from scripts import common as c
from scripts.utility.scale_image import scale_image
from scripts.editor_objects.button import Button


class ImageStoreViewer:
    def __init__(self):
        self.surf = pygame.Surface((c.width - 100, c.height - 100), pygame.SRCALPHA)
        self.title = c.editor_font.render("ImageStore contents", True, (200, 200, 205))
        self.subtitle = c.editor_font_small.render("The ImageStore object holds images so that they don't have "
                                                   "to be loaded again",
                                                   True, (120, 120, 125))
        self.subtitle2 = c.editor_font_small.render("whenever the canvas is updated. This page is a Developer Mode "
                                                    "feature.",
                                                    True, (120, 120, 125))

        self.image_list_surf = pygame.Surface((c.width - 140, c.height - 220), pygame.SRCALPHA)
        y = 0
        for image in c.image_store.element_images.keys():
            text_surf = c.editor_font_small.render(image, True, (205, 205, 255))
            icon = scale_image(c.image_store.element_images[image], 22)
            self.image_list_surf.blit(icon, (0, y + 1))
            self.image_list_surf.blit(text_surf, (30, y))
            y += 25

        self.clear_button = Button("Clear ImageStore")

    def render(self):
        self.surf.fill((50, 50, 55))
        self.surf.blit(self.title, (20, 20))
        self.surf.blit(self.subtitle, (20, 55))
        self.surf.blit(self.subtitle2, (20, 75))
        self.surf.blit(self.image_list_surf, (20, 120))

        self.clear_button.render(self.surf,(c.width-120-self.clear_button.width,c.height-150))

        c.display.blit(self.surf, (50, 50))

    def event(self, event):
        pos = (0,0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0]-50,event.pos[1]-50)

        if event.type == pygame.VIDEORESIZE:
            self.surf = pygame.Surface((c.width - 100, c.height - 100))

        if self.clear_button.click(event,pos):
            # Clear the displayed list
            self.image_list_surf = pygame.Surface((c.width - 140, c.height - 220), pygame.SRCALPHA)
            # Clear the ImageStore
            c.image_store.element_images = {}
            print("Cleared ImageStore")
