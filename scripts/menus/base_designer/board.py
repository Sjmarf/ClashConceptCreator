from scripts import common as c
from scripts.utility.file_manager import get_file_list
import pygame


class Board:
    def __init__(self):
        self.surf = pygame.Surface((c.width, c.height - 200), pygame.SRCALPHA)
        self.grid = pygame.image.load('assets/base_designer/ui/grid.png').convert_alpha()

        icons = get_file_list('assets/base_designer/ui/buildings')
        self.icons = {}
        for icon in icons:
            self.icons[icon.replace(".png", "")] = \
                pygame.image.load('assets/base_designer/ui/buildings/' + icon).convert_alpha()

        self.new_building, self.can_place = False, True
        self.board = None
        self.tile_size, self.grid_x = 0, 0
        self.invalid_positions = set()
        self.draw()

    def draw(self):
        self.invalid_positions = set()
        self.tile_size = round((c.height - 200) / 44)
        grid = pygame.transform.scale(self.grid, (round((c.height - 200) / 44) * 44, round((c.height - 200) / 44) * 44))

        # Sort keys by y value first, then x value
        all_keys = list(c.data["el"].keys())
        try:
            all_keys.sort(key=lambda xy: (xy[1], xy[0]))
        except TypeError:
            raise TypeError("'<' not supported between instances of 'int' and 'str'. all_keys: "+str(all_keys))

        # Scale icons correctly
        icons = self.icons.copy()
        for icon in self.icons.keys():
            icons[icon] = pygame.transform.scale(icons[icon], (self.tile_size * 3, self.tile_size * 3))

        # Blit icons
        icon_size = 3
        for building in all_keys:
            grid.blit(icons[c.data["el"][building]], (building[0] * self.tile_size,
                                                      building[1] * self.tile_size))
            for y in range(icon_size):
                for x in range(icon_size):
                    self.invalid_positions.add((building[0] + x, building[1] + y))

        self.board = grid

    def render(self):
        self.surf.fill((20, 20, 20))

        self.tile_size = round((c.height - 200) / 44)
        self.surf.blit(self.board, (0, 0))

        if self.new_building:
            mouse = pygame.mouse.get_pos()
            tile_x = round((mouse[0] - self.tile_size * 1.5) / self.tile_size)
            tile_y = round((mouse[1] - self.tile_size * 1.5) / self.tile_size)
            icon_name = "blank"
            self.can_place = True
            set_1 = {(tile_x, tile_y), (tile_x + 1, tile_y), (tile_x + 2, tile_y),
                     (tile_x, tile_y + 1), (tile_x + 1, tile_y + 1), (tile_x + 2, tile_y + 1),
                     (tile_x, tile_y + 2), (tile_x + 1, tile_y + 2), (tile_x + 2, tile_y + 2)}

            if len(set_1.intersection(self.invalid_positions)) > 0:
                icon_name = "red"
                self.can_place = False

            icon = pygame.transform.scale(self.icons[icon_name], (self.tile_size * 3, self.tile_size * 3))

            self.surf.blit(icon, (tile_x * self.tile_size, tile_y * self.tile_size))

        c.display.blit(self.surf, (0, 0))

    def event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.surf = pygame.Surface((c.width, c.height - 200), pygame.SRCALPHA)
            self.draw()

        if event.type == pygame.MOUSEBUTTONDOWN:
            tile_x = round((event.pos[0] - self.tile_size * 1.5) / self.tile_size)
            tile_y = round((event.pos[1] - self.tile_size * 1.5) / self.tile_size)

            if 0 <= tile_x <= 44 and 0 <= tile_y <= 44:
                # If you click on a building directly, delete it
                if (tile_x, tile_y) in c.data["el"].keys():
                    del c.data["el"][(tile_x, tile_y)]
                    self.new_building = False
                elif self.new_building:
                    if self.can_place:
                        # Add new building
                        c.data["el"][(tile_x, tile_y)] = "cannon"
                        self.new_building = False
                    else:
                        # If the new building overlaps an existing one, don't place
                        print("There is already a building there.")
                self.draw()
            else:
                pass
                #print("Invalid tile location:", tile_x, tile_y)
