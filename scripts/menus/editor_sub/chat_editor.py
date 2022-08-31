import pygame
from scripts import common as c
from scripts.utility.file_manager import getFileList
from scripts.utility.scale_image import scale_image
from scripts.editor_objects.submenu_button import SubmenuButton
from scripts.editor_objects.button import Button
from scripts.editor_objects.text_input import TextInput
from scripts.menus.editor_sub.image_selection import ImageSelection


class ChatEditor:
    def __init__(self):
        self.surf = pygame.Surface((c.width - 100, c.height - 100), pygame.SRCALPHA)
        self.sidebar = pygame.Surface((c.width-360, c.height - 100), pygame.SRCALPHA)
        self.sidebar.fill((60, 60, 65))

        self.data = c.data["el"][c.selected[0]][3]
        self.elements = []
        self.create_inputs()
        self.image_selection = ImageSelection((c.width - 500, c.height - 290))
        self.selected = [None, None, None]
        self.image_name, self.need_preview = "", False
        self.preview_img = pygame.Surface((130, 130), pygame.SRCALPHA)
        self.add_button = Button("Add New Message",width=320)
        self.add_button2 = Button("Add Empty Space", width=320)

        self.bin_button = pygame.image.load('assets/editor_gui/bin_button.png').convert_alpha()

        self.message_divider = pygame.Surface((320,1),pygame.SRCALPHA)
        self.message_divider.fill((150,150,155))
        self.scroll, self.max_scroll = 0, 0

    def create_inputs(self):
        self.elements = []
        for entry in self.data:
            if entry[0] == "EMPTY":
                row = [[TextInput(entry[1], None, label="Space Height"), "height"],
                       [TextInput(entry[2], None, label="Time", width=150), "time"],]
            else:
                row = [[TextInput(entry[1], None, label="Name"), "name"],
                       [TextInput(entry[2], None, label="Role"), "role"],
                       [TextInput(entry[3], None, width = 90), "time"],
                       [TextInput(entry[4], None, label="Message",width=320), "message"]]
                if entry[0] is None:
                    row.insert(0, [SubmenuButton("Select Icon", None, width=180), "image"])
                else:
                    row.insert(0, [SubmenuButton(entry[0], None, width=180), "image"])
            self.elements.append(row)

    def render(self):
        self.surf.fill((50, 50, 55))
        y = 20 + self.scroll
        for row in self.elements:
            self.surf.blit(self.bin_button, (310, y))
            if row[0][1] == "height":
                row[0][0].render(self.surf, (20, y))
                row[1][0].render(self.surf, (20, y+60))

                self.surf.blit(self.message_divider, (20, y + 130))
                y += 150
            else:
                row[0][0].render(self.surf, (20, y))

                row[1][0].render(self.surf, (20, y + 35))
                row[2][0].render(self.surf, (190, y + 35))
                row[3][0].render(self.surf, (210, y))
                row[4][0].render(self.surf, (20, y + 100))

                self.surf.blit(self.message_divider,(20,y + 170))
                y += 190

        self.max_scroll = y - 20 - self.scroll

        self.add_button.render(self.surf,(20,y))
        self.add_button2.render(self.surf, (20, y+40))

        self.surf.blit(self.sidebar,(360,0))
        if self.selected[0] == "image":
            self.image_selection.render(self.surf, (380, 170))
            self.surf.blit(self.preview_img, (380 + (c.width - 500) // 2 - 65, 20))

        c.display.blit(self.surf, (50, 50))

        if self.need_preview:
            if self.image_name + ".png" in getFileList('projects/' + c.project_name + '/images'):
                img = pygame.image.load('projects/' + c.project_name + '/images/' + self.image_name + ".png")
                self.preview_img = scale_image(img, 130)
                self.need_preview = False

    def event(self, event):
        pos = (0, 0)
        if event.type in {pygame.MOUSEBUTTONDOWN,pygame.MOUSEWHEEL}:
            pos = pygame.mouse.get_pos()
            pos = (pos[0] - 50, pos[1] - 50)

        if event.type == pygame.VIDEORESIZE:
            self.surf = pygame.Surface((c.width - 100, c.height - 100))
            self.image_selection.resize((c.width - 500, c.height - 290))
            self.sidebar = pygame.Surface((c.width - 360, c.height - 100), pygame.SRCALPHA)
            self.sidebar.fill((60, 60, 65))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.add_button.click(event,pos):
                self.data.append([None,"","","",""])
                self.create_inputs()
            elif self.add_button2.click(event,pos):
                self.data.append(["EMPTY","5",""])
                self.create_inputs()

            elif event.pos[0] < 320:
                if event.button == 4:
                    if self.scroll < 0:
                        self.scroll += 35
                elif event.button == 5:
                    if self.scroll > self.max_scroll * -1:
                        self.scroll -= 35

        # Left side
        y = 20 + self.scroll
        for row_num, row in enumerate(self.elements):
            # Bin button
            rect = pygame.Rect(310, y, 30, 30)
            if rect.collidepoint(pos):
                del self.data[row_num]
                self.create_inputs()
                break
            for box_num, box in enumerate(row):
                if box[1] == "image":
                    if box[0].event(event, pos):
                        self.selected = ["image", row_num, box_num]
                        # Load the correct preview image
                        self.image_selection.image_clicked = None
                        self.preview_img = pygame.Surface((130, 130), pygame.SRCALPHA)
                        if self.data[row_num][0] is not None:
                            self.image_name = self.data[row_num][0]
                            self.need_preview = True
                        return None
                else:
                    if box[0].event(event, pos):
                        # This if-statement is for the empty space height value
                        if self.data[row_num][0] == "EMPTY":
                            self.data[row_num][box_num+1] = box[0].text
                        else:
                            self.data[row_num][box_num] = box[0].text
            y += 190

        if self.selected[0] == "image":
            output = self.image_selection.event(event, pos)
            if output is not None:
                self.image_name = output[5]+output[0]
                self.need_preview = True
                self.data[self.selected[1]][0] = self.image_name
                self.create_inputs()
