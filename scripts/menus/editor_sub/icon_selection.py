import pygame
from scripts import common as c
from scripts.utility.file_manager import get_file_list, load_json
from scripts.editor_objects.button import Button
from scripts.utility.scale_image import scale_image
from _thread import start_new_thread


class IconSelection:
    def __init__(self, pos, set_path, width=300, submenu_layer=1, icon_size=50):
        self.set_path, self.pos, self.submenu_layer, self.icon_size = \
            set_path, pos, submenu_layer, icon_size
        self.surf = pygame.Surface((width, 380), pygame.SRCALPHA)
        self.icon_surf = pygame.Surface((width, 380), pygame.SRCALPHA)
        self.width = width

        self.none_button = Button("None", width=150)

        self.packs = {}
        start_new_thread(self.loadImages, ())

    def loadImages(self):
        # Used in a thread
        self.icon_surf = pygame.Surface((self.width, 380), pygame.SRCALPHA)
        enabled_packs = load_json('asset packs/enabled_packs.json')

        x, y = (20, 60)
        for pack in enabled_packs:
            icons = load_json('asset packs/' + pack + '/icon_order.json')
            x = 20
            if len(icons) > 0:
                # Render title
                text_surf = c.editor_font_small.render(pack, True, (200, 200, 205))
                self.icon_surf.blit(text_surf, (x, y))
                y += 40

                icon_list = []
                for icon in icons:
                    img = pygame.image.load('asset packs/' + pack + '/icons/' + icon + '.png')
                    img = scale_image(img, self.icon_size)
                    icon_list.append(icon)

                    self.icon_surf.blit(img, (x, y))
                    x += self.icon_size + 10
                    if x > self.width - self.icon_size:
                        x = 20
                        y += self.icon_size + 10

                y += 40

                self.packs[pack] = icon_list

    def render(self):
        self.surf.fill((50, 50, 55))
        self.none_button.render(self.surf, (self.width // 2 - 75, 20))

        x, y = (20, 60)
        if self.pos[1] + 380 > c.height:
            self.pos = [self.pos[0], c.height - 400]

        self.surf.blit(self.icon_surf, (0, 0))
        # for pack in self.packs.keys():
        # text_surf = c.editor_font_small.render(pack,True,(200,200,205))
        # x = 20
        # for icon in self.packs[pack]:
        # self.surf.blit(icon, (x, y))
        # x += self.icon_size + 10
        # if x > self.width - self.icon_size:
        # x = 20
        # y += self.icon_size + 10
        # y += 40

        c.display.blit(self.surf, self.pos)

    def event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = (20, 60)
                m_pos = (event.pos[0] - self.pos[0], event.pos[1] - self.pos[1])

                if self.none_button.click(event, m_pos):
                    self.set_element_val(None)

                for pack in self.packs.keys():
                    x = 20
                    y += 40
                    for icon in self.packs[pack]:
                        rect = pygame.Rect((x,y,self.icon_size,self.icon_size))
                        if rect.collidepoint(m_pos):
                            search_data = load_json('asset packs/' + pack + '/search_data.json')
                            name = search_data["abbreviation"]+"-"+icon
                            import shutil
                            shutil.copyfile('asset packs/'+pack+'/icons/'+icon+'.png',
                                            'projects/'+c.project_name+'/images/'+name+'.png')
                            self.set_element_val(name)

                        x += self.icon_size + 10
                        if x > self.width - self.icon_size:
                            x = 20
                            y += self.icon_size + 10
                    y += 40

    def set_element_val(self, val):
        if len(self.set_path) == 4:
            c.data["el"][self.set_path[0]][self.set_path[1]][self.set_path[2]][self.set_path[3]] = val
        elif len(self.set_path) == 3:
            c.data["el"][self.set_path[0]][self.set_path[1]][self.set_path[2]] = val
        else:
            c.data["el"][self.set_path[0]][self.set_path[1]] = val

        c.menu.canvas.draw()
        c.menu.side_bar.changeMenu()
        if self.submenu_layer == 1:
            c.submenu = None
        else:
            c.submenu2 = None
