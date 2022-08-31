from scripts import common as c
import pygame
from scripts.editor_objects.button import Button
from scripts.utility.file_manager import saveJson

class SettingLine:
    def __init__(self,text,on,switch_images):
        self.switch_images = switch_images
        self.surf = c.editor_font.render(text,True,(200,200,205))
        self.on = on
        self.pos = (0,0)

    def render(self,surf,pos):
        surf.blit(self.surf,pos)
        self.pos = pos
        surf.blit(self.switch_images[int(self.on)],(pos[0]+230,pos[1]))

    def event(self,event,pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rect = pygame.Rect(self.pos[0]+230,self.pos[1],60,30)
                if rect.collidepoint(pos):
                    self.on = not self.on
                    return True

class Settings:
    def __init__(self):
        self.title = c.editor_font_large.render("Settings", True, (250, 250, 255))
        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)
        self.asset_packs_button = Button("Asset packs",width=300)
        self.developer_settings_button = Button("Developer Settings", width=300)
        self.switch_images = [pygame.image.load('assets/editor_gui/switch_on.png').convert_alpha(),
                              pygame.image.load('assets/editor_gui/switch_off.png').convert_alpha()]

        settings = [["Developer Mode","dev_mode"]]
        self.settings = []
        self.bar = pygame.Surface((300,40))
        self.bar.fill((40,40,45))
        for setting in settings:
            self.settings.append([SettingLine(setting[0],c.settings[setting[1]],self.switch_images),setting[1]])

    def render(self):
        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)
        centre = c.width // 2 - 125

        self.surf.blit(self.title, (centre - self.title.get_width() // 2, 15))
        self.asset_packs_button.render(self.surf,(centre - 150, 80))
        y = 190
        if c.settings["dev_mode"]:
            self.developer_settings_button.render(self.surf, (centre - 150, 120))

        for setting in self.settings:
            self.surf.blit(self.bar,(centre-150,y-5))
            setting[0].render(self.surf,(centre-145,y))

        c.display.blit(self.surf, (250, 0))

    def event(self,event,pos):
        if self.asset_packs_button.click(event,pos):
            from scripts.menus.menus.asset_packs import AssetPacks
            c.menu = AssetPacks()

        if c.settings["dev_mode"]:
            if self.developer_settings_button.click(event,pos):
                from scripts.menus.main_menu_sub.dev import DevMenu
                c.menu.content = DevMenu()

        for setting in self.settings:
            if setting[0].event(event,pos):
                c.settings[setting[1]] = setting[0].on
                saveJson('data/settings.json',c.settings)
