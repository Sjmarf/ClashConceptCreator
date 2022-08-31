import pygame

from scripts import common as c
from scripts.editor_objects.button import Button

from scripts.utility.file_manager import getFileList,loadJson,saveJson
from scripts.utility.size_element import size_element
from scripts.utility.text_lines import text_lines

class AssetPacks:
    def __init__(self):
        self.back_button = Button("< Back", width=100)
        self.background = None
        self.page = None
        fade = pygame.image.load('assets/editor_gui/gradient_2.png').convert_alpha()
        self.fade = pygame.transform.scale(fade, (30, c.height))
        self.edit_button = Button("Add images",width=200)

        self.pack_buttons = []
        for pack in getFileList('asset packs'):
            if pack != ".gitkeep":
                self.pack_buttons.append([Button(pack,width=200),pack])

    def switch_page(self,pack_name):
        self.page = pack_name
        self.background = pygame.Surface((c.width-240,c.height))
        img = pygame.image.load('asset packs/'+pack_name+'/background.png').convert()
        img = pygame.transform.smoothscale(img,(img.get_width()/img.get_height()*c.height,c.height))
        self.background.blit(img,(self.background.get_width()//2-img.get_width()//2,0))

        data = loadJson('asset packs/'+pack_name+'/data.json')
        self.pack_title = size_element('assets/editor_gui/box.png',(500,110),(30,30,30,30))
        # Title
        text_surf = c.editor_font.render(data["title"],True,(250,250,255))
        self.pack_title.blit(text_surf,(250-text_surf.get_width()//2,7))
        # Subtitle
        text_surf = c.editor_font_small.render(data["subtitle"], True, (150, 150, 155))
        self.pack_title.blit(text_surf, (250 - text_surf.get_width() // 2, 36))
        # Description
        desc_surf = text_lines(data["description"],460)
        self.pack_desc = size_element('assets/editor_gui/box.png', (500, desc_surf.get_height()+80), (30, 30, 30, 30))
        self.pack_desc.blit(desc_surf,(20,20))
        # Image count
        online_images = len(loadJson('asset packs/'+pack_name+'/images.json').keys())
        local_images = len(getFileList('asset packs/'+pack_name+'/local'))
        text_surf = c.editor_font_small.render(
            'Online images: '+str(online_images)+', Local images: '+str(local_images), True, (100, 255, 255))
        self.pack_desc.blit(text_surf, (20, self.pack_desc.get_height()-30))

    def render(self):
        c.display.fill((50, 50, 55))

        self.back_button.render(c.display,(20,20))
        y = 80
        for button in self.pack_buttons:
            button[0].render(c.display,(20,y))
            y += 40

        if self.page is not None:
            c.display.blit(self.background,(240,0))
            c.display.blit(self.fade,(240,0))
            centre = ((c.width-240)//2)+240
            c.display.blit(self.pack_title,(centre-250,80))
            self.edit_button.render(c.display,(centre-100,145))
            c.display.blit(self.pack_desc, (centre - 250, 200))

    def event(self, event):
        if event.type == pygame.VIDEORESIZE:
            fade = pygame.image.load('assets/editor_gui/gradient_2.png').convert_alpha()
            self.fade = pygame.transform.scale(fade, (30, c.height))
            self.switch_page(self.page)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.click(event,event.pos):
                from scripts.menus.menus.main_menu import MainMenu
                c.menu = MainMenu(tab=4)

            for button in self.pack_buttons:
                if button[0].click(event,event.pos):
                    self.switch_page(button[1])

            if self.page is not None:
                if self.edit_button.click(event,event.pos):
                    from scripts.menus.menus.new_asset_pack_entry import NewAssetPackEntry
                    c.menu = NewAssetPackEntry(self.page)
