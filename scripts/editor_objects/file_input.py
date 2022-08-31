import pygame
from scripts import common as c

class FileInput:
    def __init__(self,text,asset_path,setting_path,mode="foreground"):
        self.img, self.pos = None, (0, 0)
        self.asset_path, self.setting_path, self.mode = asset_path, setting_path, mode
        self.HEIGHT = 30
        self.createSurface(text)

    def createSurface(self,text):
        self.img = pygame.image.load('assets/editor_gui/file_input.png').convert_alpha()
        # Load text
        raw_text_surf = c.editor_font.render(text,True,(200,200,205))
        text_surf = pygame.Surface((110,30),pygame.SRCALPHA)
        text_surf.blit(raw_text_surf,(0,0))
        fade = pygame.image.load('assets/editor_gui/text_fade.png').convert_alpha()
        text_surf.blit(fade,(80,0),special_flags=pygame.BLEND_RGBA_SUB)

        self.img.blit(text_surf,(5,1))

    def render(self,surf,pos,centre=False):
        img = self.img
        if centre:
            self.pos = (surf.get_width()//2-75,pos[1])
            surf.blit(img,(surf.get_width()//2-75,pos[1]))
        else:
            self.pos = pos
            surf.blit(img,pos)

    def event(self,event,pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            rect = pygame.Rect((self.pos[0]+120,self.pos[1],30,30))
            if rect.collidepoint(pos):
                if self.mode == "background":
                    from scripts.menus.editor_sub.background_selection import BackgroundSelection
                    c.submenu = BackgroundSelection()
                else:
                    from scripts.menus.editor_sub.file_selection import FileSelection
                    c.submenu = FileSelection(self.asset_path,self.setting_path)
