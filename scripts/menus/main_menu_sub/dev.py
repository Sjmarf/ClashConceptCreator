import pygame
import shutil
import os

from scripts import common as c
from scripts.editor_objects.button import Button
from scripts.editor_objects.text_input import TextInput
from scripts.utility.file_manager import saveJson, loadJson, getFileList


class DevMenu:
    def __init__(self):
        self.title = c.editor_font_large.render("Developer Menu", True, (250, 250, 255))
        self.subtitle = c.editor_font_small.render("Don't touch if you don't know what you're doing.", True,
                                                   (255, 150, 150))
        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)
        self.version_number = TextInput(c.VERSION, None, label="Version Number", width=300, no_editor=True)
        self.version_update_button = Button("Update All", width=300)
        self.prep_button = Button("Prep for release", width=300)

        self.back_button = Button("< Back", width=100)

    def render(self):
        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)
        centre = c.width // 2 - 125
        self.surf.blit(self.title, (centre - self.title.get_width() // 2, 15))
        self.surf.blit(self.subtitle, (centre - self.subtitle.get_width() // 2, 60))
        self.back_button.render(self.surf, (20, 20))

        self.version_number.render(self.surf, (centre - 150, 120))
        self.version_update_button.render(self.surf, (centre - 150, 190))
        self.prep_button.render(self.surf, (centre - 150, 290))

        c.display.blit(self.surf, (250, 0))

    def del_folder_contents(self, folder):
        for filename in os.listdir(folder):
            if filename not in {'.gitkeep', "projects.json"}:
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

    def event(self, event, pos):
        self.version_number.event(event, pos)

        if self.back_button.click(event, pos):
            from scripts.menus.main_menu_sub.settings import Settings
            c.menu.content = Settings()
            return

        if self.prep_button.click(event, pos):
            print("-----------\nPrepping for release...")

            saveJson('projects/projects.json', [])
            self.del_folder_contents('projects')
            print("Deleted projects")

            self.del_folder_contents('exports')
            print("Deleted exports")

            self.del_folder_contents('local images')
            print("Deleted local images")

            c.settings["dev_mode"] = False
            saveJson("data/settings.json", c.settings)
            print("Disabled developer mode")
            print("DONE")

        if self.version_update_button.click(event, pos):
            ver = self.version_number.text

            if ver not in c.settings['supported_versions']:
                c.settings['supported_versions'].append(ver)
            c.settings['version'] = ver
            c.VERSION = ver
            saveJson('data/settings.json', c.settings)
            print("Updated settings.json")
            # Update projects

            proj_list = loadJson('projects/projects.json')
            print("PROJECTS\n--------")
            for proj in proj_list:
                if type(proj) == list:
                    print("FOLDER " + proj[0])
                    for sub_proj in proj[1:]:
                        data = loadJson('projects/' + proj[0] + '/' + sub_proj + '/data.json')
                        data["version"] = ver
                        saveJson('projects/' + proj[0] + '/' + sub_proj + '/data.json', data)
                        print('updated project ' + sub_proj)
                    print("END FOLDER")

                else:
                    data = loadJson('projects/' + proj + '/data.json')
                    data["version"] = ver
                    saveJson('projects/' + proj + '/data.json', data)
                    print('updated project ' + proj)

            print("TEMPLATES\n--------")
            for template in getFileList('templates'):
                data = loadJson('templates/' + template + '/data.json')
                data["version"] = ver
                saveJson('templates/' + template + '/data.json', data)
                print("Updated template " + template)

            print("DONE")
