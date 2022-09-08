import pygame
from scripts import common as c
from scripts.utility.file_manager import get_file_list, load_json
from scripts.editor_objects.button import Button
from scripts.editor_objects.asset_pack_button import AssetPackButton


class ButtonTypeSelector:
    def __init__(self):
        self.surf = pygame.Surface((540, 500), pygame.SRCALPHA)
        self.surf.fill((50, 50, 55))
        self.switch_asset_pack(0)
        self.arrow_left = pygame.image.load('assets/editor_gui/arrow_left.png')
        self.arrow_right = pygame.image.load('assets/editor_gui/arrow_right.png')
        self.pack_num = 0

    def switch_asset_pack(self,num):
        self.pack_num = num
        data = load_json('asset packs/' + c.enabled_packs[num] + '/search_data.json')
        self.abbreviation = data["abbreviation"]
        self.asset_pack_button = AssetPackButton(c.enabled_packs[num], data["label_colour"])

        self.button_surf = pygame.Surface((540, 500), pygame.SRCALPHA)
        self.button_list = load_json('asset packs/' + c.enabled_packs[num] + '/buttons/buttons.json')["large"]
        x,y = 20,70
        for button in self.button_list:
            img = pygame.image.load('asset packs/' + c.enabled_packs[num] + '/buttons/large/'+button+'.png')
            img = pygame.transform.smoothscale(img,(110,50))
            self.button_surf.blit(img,(x,y))
            y += 70
            if y > 450:
                y = 70
                x += 130


    def render(self):
        self.surf.fill((50, 50, 55))
        # Asset pack button
        self.asset_pack_button.render(self.surf, (self.surf.get_width() // 2 - 110, 20))

        # Arrow left
        arrow_left = self.arrow_left.copy()
        if self.pack_num == 0:
            arrow_left.set_alpha(100)
        self.surf.blit(arrow_left, (self.surf.get_width() // 2 - 150, 20))
        # Arrow left
        arrow_right = self.arrow_right.copy()
        if self.pack_num == len(c.enabled_packs)-1:
            arrow_right.set_alpha(100)
        self.surf.blit(arrow_right, (self.surf.get_width() // 2 + 120, 20))

        # button surf
        self.surf.blit(self.button_surf,(0,0))
        c.display.blit(self.surf, (c.width - 560, 50))

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - (c.width - 560), event.pos[1] - 50)

            # Left arrow
            rect = pygame.Rect(self.surf.get_width() // 2 - 150, 20, 30, 30)
            if rect.collidepoint(pos):
                if self.pack_num != 0:
                    self.switch_asset_pack(self.pack_num-1)

            # Right arrow
            rect = pygame.Rect(self.surf.get_width() // 2 + 120, 20, 30, 30)
            if rect.collidepoint(pos):
                if self.pack_num != len(c.enabled_packs)-1:
                    self.switch_asset_pack(self.pack_num + 1)

            x, y = 20, 70
            for button in self.button_list:
                rect = pygame.Rect((x,y,110,50))
                if rect.collidepoint(pos):
                    self.switch(button)
                    return
                y += 70
                if y > 450:
                    y = 70
                    x += 130

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.pack_num != 0:
                    self.switch_asset_pack(self.pack_num-1)

            if event.key == pygame.K_RIGHT:
                if self.pack_num != len(c.enabled_packs)-1:
                    self.switch_asset_pack(self.pack_num + 1)

    def switch(self, button):
        new_file_name = self.abbreviation+"-"+button
        c.data["el"][c.selected[0]][3] = new_file_name
        from shutil import copyfile
        name = c.enabled_packs[self.pack_num]
        copyfile('asset packs/'+name+'/buttons/large/'+button+".png",
                 "projects/"+c.project_name+'/images/'+new_file_name+".png")
        c.menu.side_bar.changeMenu()
        c.menu.canvas.draw()
        c.submenu = None
