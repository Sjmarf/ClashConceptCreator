import pygame
from scripts import common as c

from scripts.menus.editor.canvas import Canvas
from scripts.menus.editor.bottom_bar import BottomBar
from scripts.menus.editor.side_bar import SideBar
from scripts.utility.image_store import ImageStore
from copy import deepcopy


class Editor:
    def __init__(self):
        print("editor initialised")
        self.saved_window_size = (900, 600)
        c.undo_store = deepcopy(c.data["el"])
        c.last_data = deepcopy(c.data["el"])
        c.selected = None
        c.canvas_size = [1334,750]
        # Submenu2 is used for popups inside of submenus
        c.submenu, c.submenu2 = None, None
        c.multi_select = False
        c.text_input_active = False
        self.preview_mode = False
        self.calc_sizes()

        c.image_store = ImageStore()

        self.blackout = pygame.Surface(c.display.get_size(), pygame.SRCALPHA)
        self.blackout.fill((0, 0, 0, 180))
        c.submenu_2_update, c.submenu_2_update_value = False, ""

        self.canvas = Canvas(c.sizes["canvas"])
        self.bottom_bar = BottomBar(c.sizes["bottom"])
        self.side_bar = SideBar(c.sizes["side"])
        c.unsaved_changes = False

    def calc_sizes(self):
        if self.preview_mode:
            sidebar_width = 0
            canvas = c.canvas_size
        else:
            sidebar_width = 250
            canvas = (c.width - sidebar_width, ((c.width - sidebar_width) / c.canvas_size[0]) * c.canvas_size[1])
        c.sizes = {"canvas": canvas,
                   "bottom": (c.width - sidebar_width, c.height - canvas[1]),
                   "side": (c.width - canvas[0], c.height)}

    def render(self):
        c.display.fill((0, 0, 0))

        self.canvas.render()
        self.bottom_bar.render((0, c.sizes["canvas"][1]))
        self.side_bar.render((c.sizes["canvas"][0], 0))

        if c.submenu is not None:
            self.blackout.set_alpha(180)
            c.display.blit(self.blackout, (0, 0))
            c.submenu.render()
            if c.submenu2 is not None:
                self.blackout.set_alpha(90)
                c.display.blit(self.blackout, (0, 0))
                c.submenu2.render()
        c.submenu_2_update = False

    def check_for_changes(self):
        # Used to store previous versions of the project for 'undo' feature
        if not c.last_data == c.data["el"] and self.canvas.transform is None:
            c.undo_store = deepcopy(c.last_data)
            c.last_data = deepcopy(c.data["el"])
            c.unsaved_changes = True

    def event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.calc_sizes()
            # Resize sections of screen
            if not self.preview_mode:
                self.bottom_bar.resize(c.sizes["bottom"])
                self.side_bar.resize(c.sizes["side"])
            self.canvas.size = c.sizes["canvas"]
            # Resize blackout surface
            self.blackout = pygame.Surface(c.display.get_size(), pygame.SRCALPHA)
            self.blackout.fill((0, 0, 0, 180))

        if c.submenu is None:
            self.canvas.event(event)
            if not self.preview_mode:
                self.bottom_bar.event(event)
                self.side_bar.event(event)
        else:
            if c.submenu2 is None:
                c.submenu.event(event)
            else:
                c.submenu2.event(event)

        if event.type == pygame.KEYDOWN and not c.text_input_active:
            if event.key == pygame.K_ESCAPE:
                if c.submenu is None:
                    if c.multi_select:
                        c.multi_select = False
                    c.selected, self.canvas.transform = None, None
                elif c.submenu2 is not None:
                    c.submenu2 = None
                else:
                    c.submenu = None
                    self.canvas.draw()

            elif pygame.key.get_mods():
                if event.key == pygame.K_z:
                    if len(c.data["el"]) > len(c.undo_store):
                        # Prevents a crash
                        c.selected = None
                    c.data["el"],c.undo_store = deepcopy(c.undo_store),deepcopy(c.last_data)
                    c.last_data = deepcopy(c.data["el"])
                    self.side_bar.changeMenu()
                    if c.selected is not None:
                        self.canvas.selection_pos,self.canvas.selection_size = c.data["el"][c.selected[0]][0:2]
                    self.canvas.draw(check_for_changes=False)

                elif event.key == pygame.K_s:
                    self.bottom_bar.save_project()

            elif event.key == pygame.K_f and c.submenu is None:
                self.preview_mode = not self.preview_mode
                self.calc_sizes()
                self.canvas.size = c.sizes["canvas"]
                self.canvas.draw()
                if self.preview_mode:
                    self.saved_window_size = (c.width, c.height)
                    pygame.display.set_mode(c.canvas_size)
                else:
                    pygame.display.set_mode(self.saved_window_size, pygame.RESIZABLE)
                    self.bottom_bar.resize(c.sizes["bottom"])
                    self.side_bar.resize(c.sizes["side"])
