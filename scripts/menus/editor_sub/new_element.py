import pygame
from scripts import common as c


class NewElement:
    def __init__(self, pos):
        self.pos = (pos[0], pos[1] - 300)
        self.surf = pygame.Surface((600, 380), pygame.SRCALPHA)
        self.preview_surf = pygame.Surface((256, 256), pygame.SRCALPHA)

        self.names = ['menu', 'box', 'image', 'text', 'text block', 'button', 'grid', 'tabs', 'list', 'chat',
                      'stat list', 'stat bars', 'player info', 'stars']
        self.icons = []
        for name in self.names:
            self.icons.append((pygame.image.load('assets/editor_gui/icons/' + name + '.png').convert_alpha(),
                               c.editor_font.render(name.capitalize(), True, (200, 200, 205)),
                               name))
        self.hovered = None

    def render(self):
        self.surf.fill((50, 50, 55))
        self.hovered = None
        m_pos = pygame.mouse.get_pos()
        m_pos = (m_pos[0] - self.pos[0], m_pos[1] - self.pos[1])

        x, y = 10, 10
        for icon, text, name in self.icons:
            self.surf.blit(icon, (x, y))
            self.surf.blit(text, (x + 60, y + 10))
            rect = pygame.Rect(x, y, 50, 50)
            if rect.collidepoint(m_pos):
                if self.hovered != name:
                    img = pygame.image.load('assets/element_examples/' + name + '.png').convert_alpha()
                    self.preview_surf = pygame.transform.smoothscale(img, (256, 256))
                    self.hovered = name
            y += 60
            if y > 310:
                y = 10
                x += 200

        c.display.blit(self.surf, self.pos)
        if self.hovered is not None:
            c.display.blit(self.preview_surf, (self.pos[0] + 620, self.pos[1]))

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered is not None:
                self.create_obj(self.hovered)
                c.submenu = None

    def create_obj(self, name):

        defaults = {
            # type, text, font size
            "menu": [[0, 0], [750, 750], "menu", "menu_1", "Title", "30"],
            # Type, text, font size, icon, colour
            "button": [[0, 0], [220, 60], "button", "green", "Text", "20", None, (132, 204, 44)],
            # Items, subtitle font size, icon size, icon offset, align, type
            "grid": [[0, 0], [300, 300], "grid", [], 25, 100, [0, 0], "left", "skin"],
            # Image name, image size
            "image": [[0, 0], [200, 200], "image", None, 100],
            # Text, font size, align, colour, font
            "text": [[0, 0], [200, 60], "text", "Text", 25, "centre", [255, 255, 255], "large"],
            # Type, colour, opacity
            "box": [[0, 0], [400, 400], "box", "solid", [206, 201, 195], 100],
            # Text, font size, align, text colour, font, icon size, line spacing, emoji
            "text block": [[0, 0], [300, 300], "text block", "", 25, "left", [255, 255, 255], "small", 100, 100, [[]]],
            # Tabs, selected #, Type
            "tabs": [[0, 0], [700, 100], "tabs", ["Tab1"], 0, "1"],
            # Layout (type, size in %, divider on/off), Items, Empty row (used when a new row is added), image size
            "list": [[0, 0], [500, 200], "list", [["text", 100, True]], [[["Text"]]], [["Text"]], 100],
            # Type, items (image name, label)
            "icon list": [[0, 0], [300, 100], "icon list", 1, [[None, 1]]],
            # entries, bar col
            "stat bars": [[0, 0], [450, 250], "stat bars", [[None,"",0,100]], [144,216,56], 31],
            # entries, left col, right col, left font, right font, left font size, right font size
            "stat list": [[0, 0], [450, 250], "stat list", [["stat","value"]],[51, 92, 155],[50,50,50],"small","large",20,20],
            # Items
            "chat": [[0, 0], [700, 400], "chat", [[None, "Joseph", "Member", "2m", "Text"]]],
            # name, clan, image, subtitle, align
            "player info": [[0, 0], [250, 100], "player info", None,"Name","Clan","","left"],
            # number of stars, text, type
            "stars": [[0, 0], [200, 50], "stars", "3", "", "small"]
        }


        data = defaults[name]
        # Position in centre of canvas
        data[0] = [c.canvas_size[0] / 2 - data[1][0] // 2, c.canvas_size[1] / 2 - data[1][1] // 2]
        c.data["el"].append(data)
        # Select the new element
        c.selected = [len(c.data["el"]) - 1, name]
        c.menu.canvas.selection_pos, c.menu.canvas.selection_size = c.data["el"][-1][0:2]
        # Update canvas
        c.menu.canvas.draw()
