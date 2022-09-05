import pygame
from scripts import common as c
from scripts.utility.file_manager import save_json, get_file_list
from scripts.editor_objects.button import Button
from scripts.editor_objects.small_button import SmallButton
from scripts.menus.editor_sub.new_element import NewElement
from scripts.menus.editor_sub.quit_confirm import QuitConfirm
from scripts.menus.right_click import RightClick
from copy import deepcopy


class BottomBar:
    def __init__(self, size):
        c.multi_select_elements = []
        self.mouse_pos_text = None
        self.size, self.surf, self.gradient_img, self.pos = None, None, None, (0, 0)
        self.resize(size)
        self.save_button = Button("Save", width=140)
        self.export_button = Button("Export", width=140)
        self.quit_button = Button("Quit", width=140)

        self.keybind_font = pygame.font.SysFont("Verdana", 15)
        self.mouse_pos_text = pygame.Surface((1, 1))
        self.key_img = pygame.image.load("assets/editor_gui/keys/blank.png").convert_alpha()
        self.key_shift_img = pygame.image.load("assets/editor_gui/keys/shift.png").convert_alpha()
        self.keybind_list, self.previous_kbl = None, None
        self.keybind_surf = pygame.Surface((150, size[1] - 20), pygame.SRCALPHA)

        self.add_button = Button("Add", width=140)

        self.select_button = SmallButton(icon="select_button")
        self.more_button = SmallButton(icon="more_button")

        self.mouse_pos_real = True
        self.feedback_text = [None, 0]  # Text, timer (in ticks)
        self.right_click = None

    def createKeybindSurf(self):
        self.keybind_surf = pygame.Surface((150, self.size[1] - 20), pygame.SRCALPHA)
        if self.keybind_list == "move":
            keybinds = [[["shift"], "Snap"],
                        [["X"], "Snap X axis"], [["Y"], "Snap Y axis"]]

        elif self.keybind_list == "select":
            keybinds = [[["M"],"Move"],[["shift","D"],"Duplicate"],[["X"],"Delete"],[["."], "Bring forward"],
                        [[","],"Send Backward"]]

        if self.keybind_list is not None:
            text_surf = self.keybind_font.render("Keybinds:", True, (170, 170, 175))
            self.keybind_surf.blit(text_surf, (0, 0))

            y = 30
            for keybind in keybinds:
                x = 0
                for key in keybind[0]:
                    if key == "shift":
                        self.keybind_surf.blit(self.key_shift_img, (x, y))
                    else:
                        self.keybind_surf.blit(self.key_img, (x, y))
                        icon_surf = self.keybind_font.render(key, True, (250, 250, 255))
                        pos = [x + 10 - icon_surf.get_width() // 2, y + 9 - icon_surf.get_height() // 2]
                        if key in {",", "."}:
                            pos[1] -= 6
                        self.keybind_surf.blit(icon_surf, pos)
                    x += 25
                x += 10

                text_surf = self.keybind_font.render(keybind[1], True, (120, 120, 125))
                self.keybind_surf.blit(text_surf, (x, y))
                y += 25

    def render(self, main_pos):
        if c.menu.canvas.transform == "move":
            self.keybind_list = "move"
        elif c.selected is not None:
            if c.selected[1] != "background":
                self.keybind_list = "select"
            else:
                self.keybind_list = None
        else:
            self.keybind_list = None
        if self.keybind_list != self.previous_kbl:
            self.previous_kbl = self.keybind_list
            self.createKeybindSurf()

        self.pos = main_pos
        self.surf.fill((40, 40, 45))
        self.surf.blit(self.gradient_img, (self.size[0] - 30, 0))

        if self.size[1] < 170:
            self.add_button.render(self.surf, (10, self.size[1] - 90))
            self.save_button.render(self.surf, (160, self.size[1] - 90))
            self.export_button.render(self.surf, (10, self.size[1] - 50))
            self.quit_button.render(self.surf, (160, self.size[1] - 50))
            self.surf.blit(self.keybind_surf, (330, 10))
        else:
            self.add_button.render(self.surf, (10, 10))
            self.save_button.render(self.surf, (10, self.size[1] - 130))
            self.export_button.render(self.surf, (10, self.size[1] - 90))
            self.quit_button.render(self.surf, (10, self.size[1] - 50))
            self.surf.blit(self.keybind_surf, (160, 10))

        if c.settings["dev_mode"]:
            self.more_button.render(self.surf, (self.size[0] - 40, self.size[1] - 80))
        self.select_button.render(self.surf, (self.size[0] - 40, self.size[1] - 40))

        pos = pygame.mouse.get_pos()
        if not self.mouse_pos_real:
            pos = (int(pos[0] // c.menu.canvas.scale_factor), int(pos[1] // c.menu.canvas.scale_factor))
        self.mouse_pos_text = c.editor_font.render(str(pos[0]) + "," + str(pos[1]), True, (100, 100, 105))
        self.surf.blit(self.mouse_pos_text, (self.size[0] - 10 - self.mouse_pos_text.get_width(), 10))

        fps_text = c.editor_font.render(str(c.fps), True, (100, 100, 105))
        self.surf.blit(fps_text, (self.size[0] - 10 - fps_text.get_width(), 40))

        if self.feedback_text[0] is not None:
            text_surf = c.editor_font.render(self.feedback_text[0],True,(200,200,205))
            self.surf.blit(text_surf,(self.size[0]-50-text_surf.get_width(),self.size[1]-40))
            self.feedback_text[1] -= 60/c.fps
            if self.feedback_text[1] < 0:
                self.feedback_text[0] = None

        c.display.blit(self.surf, main_pos)
        if self.right_click is not None:
            self.right_click.render(c.display,(main_pos[0]+self.size[0]-310,main_pos[1]+self.size[1]-140))

    def event(self, event):
        pos = (0, 0)
        if self.right_click is not None:
            output = self.right_click.event(event)
            if output is not None:
                if output == "image store":
                    from scripts.menus.editor_sub.dev.image_store import ImageStoreViewer
                    c.submenu = ImageStoreViewer()

                elif output == "update speed history":
                    from scripts.menus.editor_sub.dev.update_history import UpdateHistoryViewer
                    c.submenu = UpdateHistoryViewer()
                self.right_click = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - self.pos[0], event.pos[1] - self.pos[1])

            # Mouse pos readout
            rect = pygame.Rect(self.size[0] - 10 - self.mouse_pos_text.get_width(), 10,
                               self.mouse_pos_text.get_width(), self.mouse_pos_text.get_height())
            if rect.collidepoint(pos):
                self.mouse_pos_real = not self.mouse_pos_real

        if self.add_button.click(event, pos):
            c.submenu = NewElement((10, self.pos[1] - 50))

        if self.select_button.click(event, pos):
            c.multi_select = not c.multi_select
            if c.multi_select:
                self.feedback_text = ["Multi-select ON", 50]
            else:
                self.feedback_text = ["Multi-select OFF", 50]
            # Clear any existing selections
            c.selected, c.menu.canvas.transform = None, None
            c.menu.canvas.draw()

        if self.save_button.click(event, pos):
            self.save_project()

        if self.export_button.click(event, pos):
            from scripts.menus.editor_sub.export import Export
            c.submenu = Export()

        if self.quit_button.click(event, pos):
            if c.unsaved_changes:
                c.submenu = QuitConfirm()
            else:
                from scripts.menus.menus.main_menu import MainMenu
                c.menu = MainMenu()

        if c.settings["dev_mode"]:
            if self.more_button.click(event,pos):
                if self.right_click is None:
                    self.right_click = RightClick()
                    self.right_click.set_options(["update speed history","image store"],width=250,bg_col=(50,50,55))
                else:
                    self.right_click = None

    def resize(self, size):
        self.size = size
        self.surf = pygame.Surface(size, pygame.SRCALPHA)
        self.gradient_img = pygame.image.load('assets/editor_gui/gradient.png').convert_alpha()
        self.gradient_img = pygame.transform.scale(self.gradient_img, (30, size[1]))

    def save_project(self):
        if c.changed_since_opened:
            c.unsaved_changes = False
            save_json('projects/' + c.project_name + '/data.json', c.data)
            # Delete unused images
            saved_images = get_file_list('projects/' + c.project_name + '/images')
            unused_images = list(set(saved_images) - set(c.images_used))

            if ".gitkeep" in unused_images:
                unused_images.remove(".gitkeep")

            if len(unused_images) > 0:
                print("Removing " + str(len(unused_images)) + " unused images...")
                import os
                for file in unused_images:
                    os.remove('projects/' + c.project_name + '/images/' + file)
            # Save icon image
            save_json('projects/' + c.project_name + '/icon.json', c.icon_image[0])
            print("Saved")
            self.feedback_text = ["Saved",20]
            c.last_data,c.undo_store = deepcopy(c.data["el"]),deepcopy(c.data["el"])
