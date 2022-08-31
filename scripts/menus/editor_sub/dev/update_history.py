import pygame
from scripts import common as c
from scripts.utility.scale_image import scale_image
from scripts.editor_objects.button import Button
from scripts.utility.file_manager import loadJson,saveJson
from copy import copy


class UpdateHistoryViewer:
    def __init__(self):
        self.surf = pygame.Surface((c.width - 100, c.height - 100), pygame.SRCALPHA)
        self.title = c.editor_font.render("Update Speed History", True, (200, 200, 205))

        self.data = loadJson('projects/'+c.project_name+'/update_speed.json')

        # Show data for the most recent update
        self.last_update_surf = pygame.Surface((300, c.height - 220), pygame.SRCALPHA)
        if len(self.data["all"]) > 0:
            text_surf = c.editor_font_large.render(str(self.data["all"][0][1])+"s",True,(255,255,255))
            self.last_update_surf.blit(text_surf,(0,0))
            y = 100
            for entry in self.data["last"]:
                if entry[1] < 0.01:
                    col = (161, 255, 150)
                elif entry[1] < 0.02:
                    col = (244, 255, 150)
                elif entry[1] < 0.1:
                    col = (255, 215, 150)
                else:
                    col = (255, 150, 150)
                text_surf = c.editor_font_small.render(entry[0], True, (200, 200, 205))
                self.last_update_surf.blit(text_surf, (0, y))
                text_surf = c.editor_font_small.render(str(entry[1]) + "s", True, col)
                self.last_update_surf.blit(text_surf, (200 - text_surf.get_width(), y))
                y += 25

        # Render list of past updates
        self.past_updates_surf = pygame.Surface((200, c.height - 220), pygame.SRCALPHA)
        y = 0
        for entry in self.data["all"]:
            if entry[1] < 0.04:
                col = (161, 255, 150)
            elif entry[1] < 0.1:
                col = (244, 255, 150)
            elif entry[1] < 0.2:
                col = (255, 215, 150)
            else:
                col = (255, 150, 150)
            text_surf = c.editor_font_small.render(entry[0], True, (200,200,205))
            self.past_updates_surf.blit(text_surf, (0, y))
            text_surf = c.editor_font_small.render(str(entry[1])+"s", True, col)
            self.past_updates_surf.blit(text_surf, (200-text_surf.get_width(), y))
            y += 25

        self.clear_button = Button("Clear History",width=200)
        if self.data["record"]:
            self.record_button = Button("Record updates: On", width=250)
        else:
            self.record_button = Button("Record updates: Off", width=250)

    def render(self):
        self.surf.fill((50, 50, 55))
        self.surf.blit(self.title, (20, 20))
        self.surf.blit(self.past_updates_surf, (c.width-320, 20))
        self.surf.blit(self.last_update_surf, (20, 80))

        self.clear_button.render(self.surf,(c.width-320,c.height-150))
        self.record_button.render(self.surf,(c.width-590,c.height-150))

        c.display.blit(self.surf, (50, 50))

    def event(self, event):
        pos = (0,0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0]-50,event.pos[1]-50)

        if event.type == pygame.VIDEORESIZE:
            self.surf = pygame.Surface((c.width - 100, c.height - 100))

        if self.clear_button.click(event,pos):
            # Clear the displayed list
            self.past_updates_surf = pygame.Surface((c.width - 140, c.height - 220), pygame.SRCALPHA)
            self.last_update_surf = pygame.Surface((300, c.height - 220), pygame.SRCALPHA)
            self.data["all"] = []
            self.data["last"] = []
            saveJson('projects/'+c.project_name+'/update_speed.json',self.data)
            print("Cleared update history for this project")

        if self.record_button.click(event,pos):
            self.data["record"] = not self.data["record"]
            if self.data["record"]:
                self.record_button = Button("Record updates: On", width=250)
            else:
                self.record_button = Button("Record updates: Off", width=250)
            saveJson('projects/' + c.project_name + '/update_speed.json', self.data)
