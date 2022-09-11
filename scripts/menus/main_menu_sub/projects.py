import pygame

from scripts import common as c
from scripts.editor_objects.button import Button
from scripts.utility.file_manager import load_json, save_json, get_file_list
from scripts.menus.right_click import RightClick
from scripts.utility import main_menu_actions
from scripts.utility.scale_image import scale_image
from scripts.editor_objects.text_input import TextInput
from scripts.editor_objects.scrollbar import Scrollbar


class NewProject:
    def __init__(self):
        self.title = c.editor_font.render("Choose a template:", True, (200, 200, 205))
        self.blank_surf = pygame.Surface((200, 150), pygame.SRCALPHA)
        self.thumbnails = {}
        for i in get_file_list('assets/template_thumbnails'):
            name = i.replace(".png", "")
            surf = self.blank_surf.copy()
            img = pygame.image.load("assets/template_thumbnails/" + i).convert()
            surf.blit(img, (0, 0))
            text_surf = c.editor_font.render(name.title(), True, (200, 200, 205))
            surf.blit(text_surf, (100 - text_surf.get_width() // 2, 120))
            self.thumbnails[name] = surf

        self.rows = ["troop", "magic items", "magic item info","magic item sell"]

    def render(self, surf):
        surf.blit(self.title, (surf.get_width() // 2 - self.title.get_width() // 2, 20))
        surf.blit(self.thumbnails["blank"], (20, 80))

        x, y = 20, 250
        for row in self.rows:
            surf.blit(self.thumbnails[row], (x, y))
            x += 230
            if x > c.width - 450:
                x = 20
                y += 160

    def event(self, event, pos):
        rect = pygame.Rect((20, 80, 200, 150))
        if rect.collidepoint(pos):
            self.new_project("blank")
            return None

        if c.settings["dev_mode"]:
            rect = pygame.Rect((250, 80, 200, 150))
            if rect.collidepoint(pos):
                self.new_project("base design")
                return None

        x, y = 20, 250
        for row in self.rows:
            rect = pygame.Rect((x, y, 200, 150))
            if rect.collidepoint(pos):
                self.new_project(row)
                return None
            x += 230
            if x > c.width - 450:
                x = 20
                y += 160

    def new_project(self, template):
        print(template)
        proj_name = "Project " + str(len(c.menu.content.project_data) + 1)
        from shutil import copytree, ignore_patterns
        copytree('templates/' + template, 'projects/' + proj_name, ignore=ignore_patterns(".DS_Store"))
        c.menu.content.project_data.insert(0, proj_name)
        save_json('projects/projects.json', c.menu.content.project_data)
        c.menu.content.open_project(proj_name, 0)


class Delete:
    def __init__(self, name, data):
        self.name, self.data = name, data
        self.text = c.editor_font.render("Are you sure you want to delete " + name + "?", True, (200, 200, 205))
        self.back_button = Button("No, take me back", width=300)
        self.del_button = Button("Delete", width=300)

    def render(self, surf):
        surf.blit(self.text, (surf.get_width() // 2 - self.text.get_width() // 2, 200))
        self.back_button.render(surf, (surf.get_width() // 2 - 150, 240))
        self.del_button.render(surf, (surf.get_width() // 2 - 150, 280))

    def event(self, event, pos):
        if self.del_button.click(event, pos):
            main_menu_actions.delete(self.data, self.name)
            c.menu.content.create_rows()
            c.menu.content.submenu = None
        if self.back_button.click(event, pos):
            c.menu.content.submenu = None


class Move:
    def __init__(self, name):
        self.is_folder = False
        if "/" in name:
            name = name.split("/")[1]
            self.is_folder = True
        self.name = name
        self.none_button = Button("No folder", width=300)
        self.none_button = Button("No folder", width=300)
        data = c.menu.content.project_data
        self.buttons = []
        for i in data:
            if type(i) == list:
                self.buttons.append([Button(i[0], width=300), i[0]])

    def render(self, surf):
        self.none_button.render(surf, (surf.get_width() // 2 - 150, 200))
        y = 250
        for button in self.buttons:
            button[0].render(surf, (surf.get_width() // 2 - 150, y))
            y += 40

    def event(self, event, pos):
        data = c.menu.content.project_data
        if self.none_button.click(event, pos):
            print(data)
            path = self.find_and_remove()
            from shutil import move
            move('projects/' + path, 'projects/' + self.name)
            data.insert(0, self.name)
            print(data)
            self.close_menu()

        else:
            for button in self.buttons:
                if button[0].click(event, pos):
                    path = self.find_and_remove()
                    from shutil import move
                    move('projects/' + path, 'projects/' + button[1] + "/" + self.name)
                    for num, i in enumerate(data):
                        if type(i) == list:
                            if i[0] == button[1]:
                                data[num].insert(1, self.name)
                    self.close_menu()
                    break

        # del data[data.index(self.name)]

    def close_menu(self):
        save_json('projects/projects.json', c.menu.content.project_data)
        c.menu.content.create_rows()
        c.menu.content.submenu = None

    def find_and_remove(self):
        data = c.menu.content.project_data
        for num, i in enumerate(data):

            if i == self.name:
                del data[num]
                return i

            elif type(i) == list:
                for num2, j in enumerate(i[1:]):
                    if j == self.name:
                        del data[num][num2 + 1]
                        return i[0] + "/" + j


class Rename:
    def __init__(self, name):
        self.is_folder, self.folder_prefix = False, ""
        if "FOLDER" in name:
            name = name.replace("FOLDER ", "")
            self.is_folder = True
        if "/" in name:
            self.folder_prefix, name = name.split("/")
        self.old_name = name
        self.input = TextInput(name, None, width=300, no_editor=True)
        self.done_button = Button("Done", width=300)

    def render(self, surf):
        self.input.render(surf, (surf.get_width() // 2 - 150, 200))
        self.done_button.render(surf, (surf.get_width() // 2 - 150, 240))

    def event(self, event, pos):
        self.input.event(event, pos)
        if self.done_button.click(event, pos):
            data = c.menu.content.project_data
            from shutil import move
            if self.folder_prefix != "":
                for i in data:
                    if type(i) == list:
                        if i[0] == self.folder_prefix:
                            for num2,j in enumerate(i[1:]):
                                if j == self.old_name:
                                    i[num2+1] = self.input.text
                                    move('projects/' + self.folder_prefix + "/" + self.old_name,
                                         'projects/' + self.folder_prefix + "/" + self.input.text)
            elif not self.is_folder:
                data[data.index(self.old_name)] = self.input.text
                move('projects/' + self.old_name, 'projects/' + self.input.text)

            else:
                for i in data:
                    if type(i) == list:
                        if i[0] == self.old_name:
                            i[0] = self.input.text
                            break
                move('projects/' + self.old_name, 'projects/' + self.input.text)

            save_json('projects/projects.json', c.menu.content.project_data)
            c.menu.content.create_rows()
            c.menu.content.submenu = None


class Projects:
    def __init__(self):
        self.title = c.editor_font_large.render("Projects", True, (250, 250, 255))
        self.project_data = load_json('projects/projects.json')
        self.new_proj_button = Button('New Project', width=240)
        self.new_folder_button = Button('New Folder', width=240)

        self.rows = []
        self.create_rows()
        self.right_click = RightClick()
        self.right_click_shown = False
        self.right_click_pos, self.right_click_proj = (0, 0), ""

        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)
        self.submenu = None
        self.scrollbar = Scrollbar()

    def render(self):
        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)

        if self.submenu is None:
            centre = c.width // 2 - 125
            self.surf.blit(self.title, (centre - self.title.get_width() // 2, 15 - self.scrollbar.scroll))

            self.new_proj_button.render(self.surf, (centre - 250, 70 - self.scrollbar.scroll))
            self.new_folder_button.render(self.surf, (centre + 10, 70 - self.scrollbar.scroll))

            y = 120 - self.scrollbar.scroll
            for row in self.rows:
                self.surf.blit(row[0], (centre - 250, y))
                y += 60
                if "FOLDER" in row[1]:
                    if row[2]:
                        for proj in row[3]:
                            self.surf.blit(proj[0], (centre - 150, y))
                            y += 60
                        y += 10

            self.scrollbar.set_height(c.height - 20, y + self.scrollbar.scroll + 100)
            self.scrollbar.render(self.surf, (c.width - 275, 10))

        else:
            self.submenu.render(self.surf)

        c.display.blit(self.surf, (250, 0))
        if self.right_click_shown:
            self.right_click.render(c.display, self.right_click_pos)

    def create_rows(self):
        bar_img = pygame.image.load('assets/editor_gui/main_menu/project_box.png').convert_alpha()
        bar_small_img = pygame.image.load('assets/editor_gui/main_menu/project_box_small.png').convert_alpha()
        folder_icon = pygame.image.load('assets/editor_gui/main_menu/folder_icon.png').convert_alpha()

        self.rows = []
        for line in self.project_data:
            img = bar_img.copy()
            if type(line) == str:
                img = self.createRowImage(img, line, 'projects/' + line)
                self.rows.append([img, line])
            else:
                text_surf = c.editor_font.render(line[0], True, (200, 200, 205))
                img.blit(folder_icon, (0, 0))
                img.blit(text_surf, (65, 12))
                contents = []
                folder_name = line[0].replace("FOLDER ", "")
                for proj in line[1:]:
                    small_img = bar_small_img.copy()
                    small_img = self.createRowImage(small_img, proj, 'projects/' + folder_name + '/' + proj)
                    contents.append((small_img, proj))
                self.rows.append([img, "FOLDER " + line[0], False, contents])

    def createRowImage(self, img, title, proj_path):
        text_surf = c.editor_font.render(title, True, (200, 200, 205))
        img.blit(text_surf, (65, 12))
        icon_name = load_json(proj_path + '/icon.json')

        if icon_name is not None:
            try:
                icon = pygame.image.load(proj_path + '/images/' + icon_name).convert_alpha()
            except FileNotFoundError:
                icon = pygame.image.load('assets/editor_gui/error.png').convert_alpha()
            icon = scale_image(icon, 40)
            img.blit(icon, (25 - icon.get_width() // 2, 25 - icon.get_height() // 2))
        return img

    def event(self, event, pos):

        if self.submenu is None:
            self.scrollbar.event(event, pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.right_click_shown:
                    rc_output = self.right_click.event(event,event.pos)

                    if type(rc_output) == str:
                        if rc_output == "delete":
                            self.submenu = Delete(self.right_click_proj, self.project_data)

                        elif rc_output == "duplicate":
                            main_menu_actions.duplicate(self.project_data, self.right_click_proj)
                            self.create_rows()

                        elif rc_output == "rename":
                            self.submenu = Rename(self.right_click_proj)

                        elif rc_output == "move":
                            self.submenu = Move(self.right_click_proj)

                        self.right_click_shown = False

                    elif rc_output:
                        self.right_click_shown = False

                elif self.new_proj_button.click(event, pos):
                    # Create new project
                    self.submenu = NewProject()
                elif self.new_folder_button.click(event, pos):
                    # Create new folder
                    print('New folder')
                    folder_name = "Folder " + str(len(self.project_data) + 1)
                    self.project_data.append([folder_name])
                    save_json('projects/projects.json', self.project_data)
                    from os import makedirs, getcwd
                    makedirs(getcwd() + '/projects/' + folder_name)
                    self.create_rows()
                else:

                    centre = c.width // 2 - 125
                    y = 120 - self.scrollbar.scroll
                    for row_num, row in enumerate(self.rows):
                        rect = pygame.Rect(centre - 250, y, 500, 50)

                        if rect.collidepoint(pos):
                            if event.button == 3 or (event.button == 1 and pygame.key.get_mods() == 64):
                                # Detect ctrl+click also /\
                                if "FOLDER" in row[1]:
                                    self.right_click.set_options(["rename", "delete"])
                                else:
                                    self.right_click.set_options(["rename", "move", "duplicate", "delete"])
                                self.right_click_proj = row[1]
                                self.right_click_shown = True
                                self.right_click_pos = event.pos

                            elif event.button == 1:
                                if "FOLDER" in row[1]:
                                    row[2] = not row[2]
                                else:
                                    self.open_project(row[1], row_num)

                        y += 60
                        if "FOLDER" in row[1]:
                            if row[2]:
                                for proj in row[3]:
                                    rect = pygame.Rect(centre - 150, y, 500, 50)
                                    if rect.collidepoint(pos):
                                        folder_name = row[1].replace("FOLDER ", "")
                                        if event.button == 1:
                                            self.open_project(folder_name + "/" + proj[1], row_num)
                                        elif event.button == 3:
                                            self.right_click_proj = (folder_name + "/" + proj[1])
                                            self.right_click.set_options(["rename", "move", "duplicate", "delete"])
                                            self.right_click_shown = True
                                            self.right_click_pos = pos
                                    y += 60
                                y += 10

        else:
            pos = (0, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = (event.pos[0] - 250, event.pos[1])

            self.submenu.event(event, pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.submenu = None

    def open_project(self, name, row_num):
        # Move project to top of list
        data = self.project_data.pop(row_num)
        self.project_data.insert(0, data)
        save_json('projects/projects.json', self.project_data)

        # Check project type
        if 'project_type.json' in get_file_list('projects/' + name):
            proj_type = load_json('projects/' + name + '/project_type.json')["proj_type"]
        else:
            print("No project_type.json found, creating one...")
            from shutil import copyfile
            copyfile('templates/blank/project_type.json','projects/' + name + '/project_type.json')
            proj_type = "menu"

        # Load data
        c.project_name = name
        c.data = load_json('projects/' + name + '/data.json')
        c.enabled_packs = load_json('asset packs/enabled_packs.json')

        supported_versions = c.settings["supported_versions"]
        if c.data["version"] == c.VERSION:
            # Open editor
            if proj_type == "menu":
                from scripts.menus.menus.editor import Editor
                c.menu = Editor()

        elif c.data["version"] in supported_versions:
            # Show project update screen
            from scripts.menus.menus.project_update_menu import ProjectUpdate
            c.menu = ProjectUpdate(name, ver=c.data["version"])
        else:
            # If the project version isn't supported on this version, show error screen
            from scripts.menus.menus.project_load_error import ProjectLoadError
            c.menu = ProjectLoadError(ver=c.data["version"], supported=", ".join(supported_versions))
