import pygame
from scripts import common as c
from scripts.editor_objects.button import Button
from scripts.editor_objects.submenu_button import SubmenuButton
from scripts.editor_objects.text_input import TextInput
from scripts.menus.editor_sub.image_selection import ImageSelection
from scripts.utility.file_manager import getFileList
from scripts.utility.scale_image import scale_image
from copy import deepcopy


class ListEntriesEditor:
    def __init__(self):
        self.surf = pygame.Surface((c.width - 100, c.height - 100), pygame.SRCALPHA)
        self.row_img = pygame.image.load('assets/editor_gui/list/row.png').convert_alpha()
        self.parts, self.rows = c.data["el"][c.selected[0]][3:5]
        self.image_selection = ImageSelection((c.width-520,c.height-240))

        self.bin_img = pygame.image.load('assets/editor_gui/bin_button.png').convert_alpha()
        self.add_button = Button("New Row",width=300)
        self.back_button = Button("< Back",width=100)
        self.image_name, self.need_preview = "",False
        self.preview_img = pygame.Surface((80,80),pygame.SRCALPHA)

        self.part_buttons = []
        self.selected, self.image_editing = 0, None
        self.scroll, self.max_scroll = 0, 0
        self.switch_selected(0)
        self.render_row_titles()

    def render_row_titles(self):
        # The first 'text' or 'double text' part is used as the row title
        self.row_titles = []
        index = None
        for num,part in enumerate(self.parts):
            if part[0] in {"text","double text"}:
                index = num
                break

        if index is None:
            for row in self.rows:
                self.row_titles.append(None)
        else:
            for row in self.rows:
                text = row[index][0]
                text_surf = c.editor_font.render(text,True,(200,200,205))
                self.row_titles.append(text_surf)

    def switch_selected(self,row):
        self.selected = row
        self.part_buttons = []
        num = 0
        width = c.width - 550
        for part, item in zip(self.parts,self.rows[row]):
            if part[0] == "text":
                self.part_buttons.append([TextInput(item[0], None, label="Text",width=width),"text",num])
            elif part[0] == "image":
                if item[0] is None:
                    self.part_buttons.append([SubmenuButton("Select Image", None, width=width),"image",num])
                else:
                    self.part_buttons.append([SubmenuButton(item[0], None, width=width),"image",num])
            elif part[0] == "double text":
                self.part_buttons.append([TextInput(item[0], None, label="Text 1",width=width), "double text", num])
                self.part_buttons.append([TextInput(item[1], None, label="Text 2",width=width), "double text", num])
            elif part[0] == "counter":
                self.part_buttons.append([TextInput(item[0], None, label="Counter Label",width=width), "counter", num])
                self.part_buttons.append([TextInput(item[1], None, label="Counter Value",width=width), "counter", num])
            elif part[0] == "readout":
                self.part_buttons.append([TextInput(item[0], None, label="Readout Value",width=width),"readout",num])
            num += 1

    def render(self):
        self.surf.fill((50, 50, 55))
        y = 20
        for title,row in zip(self.row_titles,self.rows):
            self.surf.blit(self.row_img,(20,y))
            if len(self.rows) > 1:
                self.surf.blit(self.bin_img,(330,y+4))
            if title is not None:
                self.surf.blit(title,(30,y+6))
            y += 50

        self.add_button.render(self.surf, (20, y))

        if self.image_editing is not None:
            self.image_selection.render(self.surf,(400,120), scrollbar_mouse_y_offset=-50)
            self.surf.blit(self.preview_img,(c.width-200,20))
            self.back_button.render(self.surf,(400,20))

        else:
            text_surf = c.editor_font.render("Row "+str(self.selected+1),True,(200,200,205))
            self.surf.blit(text_surf,(400+(c.width-550)//2-text_surf.get_width()//2,20+self.scroll))
            y = 60+self.scroll
            for i in self.part_buttons:
                i[0].render(self.surf,(400,y))
                y += i[0].HEIGHT + 10
            self.max_scroll = y-self.scroll-60-(c.height-200)

        if self.need_preview:
            if self.image_name + ".png" in getFileList('projects/' + c.project_name + '/images'):
                img = pygame.image.load('projects/' + c.project_name + '/images/' + self.image_name + ".png")
                self.preview_img = scale_image(img, 80)
                self.need_preview = False

        c.display.blit(self.surf, (50, 50))

    def event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        pos = (mouse_pos[0] - 50, mouse_pos[1] - 50)
        if self.image_editing is not None:
            if self.back_button.click(event,pos):
                self.image_editing = None

            output = self.image_selection.event(event, pos)
            if output != self.image_name and output is not None:
                self.image_name = output[5] + output[0]
                self.need_preview = True
                self.rows[self.selected][self.image_editing][0] = output[5] + output[0]
                self.switch_selected(self.selected)

        if event.type == pygame.VIDEORESIZE:
            self.surf = pygame.Surface((c.width - 100, c.height - 100))
            self.image_selection.resize((c.width - 520, c.height - 240))
            self.switch_selected(self.selected)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.add_button.click(event,pos):
                self.rows.append(deepcopy(c.data["el"][c.selected[0]][5]))
                self.render_row_titles()
                return None

            else:
                if event.button == 1:
                    y = 20
                    for num,row in enumerate(self.rows):
                        rect = pygame.Rect(20,y,300,40)
                        if rect.collidepoint(pos):
                            print(num)
                            self.switch_selected(num)
                            self.image_name, self.need_preview, self.image_editing = "", False, None
                            return None

                        if len(self.rows) > 1:
                            rect = pygame.Rect(330,y+4,30,30)
                            if rect.collidepoint(pos):
                                del self.rows[num]
                                self.switch_selected(0)
                                self.render_row_titles()
                                return None

                        y += 50
                elif event.button == 4:
                    if self.scroll < 0:
                        self.scroll += 15
                elif event.button == 5:
                    if self.scroll > self.max_scroll*-1:
                        self.scroll -= 15

        for item in self.part_buttons:
            if item[1] == "text":
                if item[0].event(event,pos):
                    self.rows[self.selected][item[2]][0] = item[0].text
                    self.render_row_titles()

            elif item[1] == "image":
                if item[0].event(event,pos):
                    self.image_editing = item[2]
                    self.image_name, self.need_preview = "", False
                    if self.rows[self.selected][item[2]][0] is not None:
                        self.image_name, self.need_preview = self.rows[self.selected][item[2]][0], True
                    self.preview_img = pygame.Surface((80,80),pygame.SRCALPHA)

            elif item[1] == "double text":
                if item[0].event(event,pos):
                    if item[0].label == "Text 1":
                        self.rows[self.selected][item[2]][0] = item[0].text
                        self.render_row_titles()
                    else:
                        self.rows[self.selected][item[2]][1] = item[0].text

            elif item[1] == "counter":
                if item[0].event(event,pos):
                    if item[0].label == "Counter Label":
                        self.rows[self.selected][item[2]][0] = item[0].text
                    else:
                        self.rows[self.selected][item[2]][1] = item[0].text
            elif item[1] == "readout":
                if item[0].event(event,pos):
                    self.rows[self.selected][item[2]][0] = item[0].text
