from scripts import common as c
from scripts.utility.file_manager import get_file_list
import pygame


class Scenery:
    def __init__(self):
        self.surf = pygame.Surface((c.width, c.height - 200), pygame.SRCALPHA)
        self.background = pygame.image.load('assets/base_designer/scenery/classic.png').convert_alpha()

        self.canvas = None
        self.canvas_size = self.background.get_size()
        self.canvas_zoom = 0.2
        self.canvas_pos = [0, 0]  # [self.canvas_size[0]//-2+c.width//2,self.canvas_size[1]//-2+(c.height-200)//2]
        print(self.canvas_pos)
        self.dragging, self.dragging_start_pos, self.dragging_mouse_pos = False, (0, 0), (0, 0)
        self.draw()

    def draw(self):
        self.canvas = self.background.copy()
        c.image_store.element_images_used, c.images_used = [], []

        # Sort keys by y value first, then x value
        all_keys = list(c.data["el"].keys())
        all_keys.sort(key=lambda xy: (xy[1], xy[0]))

        tile_size = 170
        start_pos = (self.canvas_size[0]//2, 270)
        tile_spacing_multiplier = 20

        # Blit buildings
        for building in all_keys:
            img = c.image_store.get_scaled_image("assets/base_designer/bases/capital_3x3.png",
                                                 tile_size)
            #img = c.image_store.get_scaled_image("assets/base_designer/buildings/" + c.data["el"][building] + ".png",
                                                 #tile_size)
            pos = (building[0] * tile_spacing_multiplier, building[1] * tile_spacing_multiplier)
            self.canvas.blit(img, (start_pos[0] + pos[0] - pos[1],
                                   start_pos[1] + pos[1] + pos[0]))

        c.image_store.clear_unused_images()

    def render(self):
        self.surf.fill((20, 20, 20))
        canvas = pygame.transform.scale(self.canvas, (self.canvas_size[0] * self.canvas_zoom,
                                                      self.canvas_size[1] * self.canvas_zoom))

        self.surf.blit(canvas, ((self.canvas_pos[0] * self.canvas_zoom,
                                 self.canvas_pos[1] * self.canvas_zoom)))

        c.display.blit(self.surf, (0, 0))

        if self.dragging:
            mouse = pygame.mouse.get_pos()
            self.canvas_pos = [self.dragging_start_pos[0] + (mouse[0] - self.dragging_mouse_pos[0]) / self.canvas_zoom,
                               self.dragging_start_pos[1] + (mouse[1] - self.dragging_mouse_pos[1]) / self.canvas_zoom]

    def event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.surf = pygame.Surface((c.width, c.height - 200), pygame.SRCALPHA)
            self.draw()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # If clicking on the canvas area and not the bottom bar
            if event.pos[1] < c.height - 200:
                self.dragging = True
                self.dragging_start_pos = self.canvas_pos
                self.dragging_mouse_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                # Zoom in
                self.canvas_zoom += 0.1

            elif event.key == pygame.K_MINUS:
                # Zoom out
                self.canvas_zoom -= 0.1

        if event.type == pygame.MOUSEWHEEL:
            self.canvas_pos[0] -= event.x / self.canvas_zoom * 10
            self.canvas_pos[1] += event.y / self.canvas_zoom * 10
