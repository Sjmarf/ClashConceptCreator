import pygame
from scripts import common as c
from scripts.editor_objects.button import Button
from scripts.editor_objects.small_button import SmallButton
from scripts.editor_objects.text_input import TextInput
from scripts.menus.editor_sub.image_selection import ImageSelection
from scripts.utility.scale_image import scale_image
from scripts.utility.file_manager import getFileList


class GridEditor:
    def __init__(self):
        self.element = c.selected[0]
        self.surf = pygame.Surface((c.width - 100, c.height - 100), pygame.SRCALPHA)
        self.sidebar = pygame.Surface((420, c.height - 100), pygame.SRCALPHA)
        self.sidebar.fill((45, 45, 50))

        self.row_img = pygame.image.load('assets/editor_gui/grid/row.png').convert_alpha()
        self.title_row_img = pygame.image.load('assets/editor_gui/grid/title_row.png').convert_alpha()

        self.grid_images = {0: pygame.image.load('assets/editor_gui/grid/box_0.png').convert_alpha(),
                            1: pygame.image.load('assets/editor_gui/grid/box_1.png').convert_alpha(),
                            2: pygame.image.load('assets/editor_gui/grid/box_2.png').convert_alpha()}
        self.new_box_img = pygame.image.load('assets/editor_gui/grid/box_new.png').convert_alpha()

        self.reorder_bar = pygame.Surface((300, 5), pygame.SRCALPHA)
        self.reorder_bar.fill((200, 200, 205))

        self.bin_button = pygame.image.load('assets/editor_gui/bin_button.png').convert_alpha()
        self.reorder_button = pygame.image.load('assets/editor_gui/reorder.png').convert_alpha()

        self.new_row_button = Button("+ Row", width=145)
        self.new_title_button = Button("+ Subtitle", width=145)

        self.reorder, self.reorder_num = None, 0
        self.edit = None
        self.need_preview = False

        self.delete_box_button = SmallButton()
        self.title_text, self.box_preview = None, None
        self.image_selection = ImageSelection(size=(c.width - 600, c.height - 300))

    def render(self):
        self.surf.fill((55, 55, 60))
        self.surf.blit(self.sidebar, (0, 0))
        data = c.data["el"][self.element]

        # LEFT SIDE
        # -------------------
        # Reorder bar
        snap_lines = [43]
        y = 43
        if self.reorder is not None:
            for row in data[3]:
                if len(row) > 0:
                    if type(row[0]) == str:
                        y += 50
                    else:
                        y += 70
                    snap_lines.append(y)
            mouse_y = pygame.mouse.get_pos()[1] - 50
            reorder_y = min(snap_lines, key=lambda m_y: abs(m_y - mouse_y))
            self.reorder_num = snap_lines.index(reorder_y)
            self.surf.blit(self.reorder_bar, (50, reorder_y))

        x, y = 50, 50
        for row in data[3]:
            if len(row) > 0:
                if type(row[0]) == str:
                    self.surf.blit(self.title_row_img, (50, y))
                    text_surf = c.editor_font.render(row[0], True, (200, 200, 205))
                    self.surf.blit(text_surf, (60, y + 7))
                    # Bin button
                    self.surf.blit(self.bin_button, (360, y + 6))
                    # Reorder button
                    self.surf.blit(self.reorder_button, (10, y + 6))
                    y += 50
                else:
                    # Background
                    self.surf.blit(self.row_img, (50, y))
                    x = 60
                    # Boxes
                    for box in row:
                        self.surf.blit(self.grid_images[box[1]], (x, y + 10))
                        x += 50
                    # New Box button
                    if len(row) < 5:
                        self.surf.blit(self.new_box_img, (x, y + 10))
                    # Bin button
                    self.surf.blit(self.bin_button, (360, y + 17))
                    # Reorder button
                    self.surf.blit(self.reorder_button, (10, y + 17))
                    y += 70
        self.new_row_button.render(self.surf, (50, y))
        self.new_title_button.render(self.surf, (205, y))

        # RIGHT SIDE
        # -------------------
        if self.edit is not None:
            centre = 420 + (c.width - 520) // 2
            text_surf = c.editor_font.render(self.edit[0].capitalize(), True, (200, 200, 205))
            self.surf.blit(text_surf, (centre - text_surf.get_width() // 2, 15))

            if self.edit[0] == "box":
                self.delete_box_button.render(self.surf, (c.width - 145, 15))
                self.surf.blit(self.box_preview, (centre - self.image_selection.size[0] // 2, 50))
                self.image_selection.render(self.surf, (centre - self.image_selection.size[0] // 2, 170),
                                            scrollbar_mouse_y_offset=-50)
                # Frame options
                positions = [(0,0),(50,0),(0,50),(50,50)]
                for num in self.grid_images.keys():
                    pos = positions[num]
                    self.surf.blit(self.grid_images[num],(c.width-240+pos[0],70+pos[1]))
                # Attempt to load preview image if it isn't already loaded
                if self.need_preview:
                    self.attemptPreviewLoad()

            else:
                self.title_text.render(self.surf, (centre - 75, 50))

        c.display.blit(self.surf, (50, 50))

    def switchEditor(self, data):
        self.edit = data
        if data[0] == "title":
            self.title_text = TextInput(c.data["el"][self.element][3][self.edit[1]][0], None)
        else:
            self.box_preview = pygame.Surface((110, 110), pygame.SRCALPHA)
            self.attemptPreviewLoad()

    def attemptPreviewLoad(self):
        image_name = c.data["el"][self.element][3][self.edit[1]][self.edit[2]][0]
        if image_name is None:
            self.need_preview = False
        else:
            image_name += ".png"
            if image_name in getFileList('projects/' + c.project_name + '/images'):
                img = pygame.image.load('projects/' + c.project_name + '/images/' + image_name)
                self.box_preview = scale_image(img, 110)
                self.need_preview = False
            else:
                self.need_preview = True

    def event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0] - 50, mouse_pos[1] - 50)

        if self.edit is not None:
            if self.edit[0] == "title":
                if self.title_text.event(event, mouse_pos):
                    c.data["el"][self.element][3][self.edit[1]][0] = self.title_text.text
            else:
                output = self.image_selection.event(event, mouse_pos)
                if output is not None:
                    output, local = output[5]+output[0], output[4]
                    c.data["el"][self.element][3][self.edit[1]][self.edit[2]][0] = output
                    self.attemptPreviewLoad()

        if event.type == pygame.VIDEORESIZE:
            self.surf = pygame.Surface((c.width - 100, c.height - 100))
            self.sidebar = pygame.Surface((420, c.height - 100), pygame.SRCALPHA)
            self.sidebar.fill((45, 45, 50))
            self.image_selection.resize((c.width - 600, c.height - 300))

        if event.type == pygame.MOUSEBUTTONUP:
            if self.reorder is not None:
                row = c.data["el"][self.element][3].pop(self.reorder)
                c.data["el"][self.element][3].insert(self.reorder_num, row)
            self.reorder = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            # LEFT SIDE
            # ----------------

            if mouse_pos[0] < 420:
                if self.new_row_button.click(event, mouse_pos):
                    if len(c.data["el"][self.element][3]) == 0:
                        # Create a ticked box if there are not any rows yet
                        c.data["el"][self.element][3].append([[None, 1]])
                    else:
                        c.data["el"][self.element][3].append([[None, 0]])
                elif self.new_title_button.click(event, mouse_pos):
                    c.data["el"][self.element][3].append(["Subtitle"])

                else:
                    x, y = 50, 50
                    for row_num, row in enumerate(c.data["el"][self.element][3]):
                        x = 50
                        if len(row) > 0:
                            if type(row[0]) == str:
                                rect = pygame.Rect(x, y, 300, 40)
                                if rect.collidepoint(mouse_pos):
                                    self.switchEditor(["title", row_num])
                                # Subtitle delete button
                                rect = pygame.Rect(360, y + 6, 30, 30)
                                if rect.collidepoint(mouse_pos):
                                    del c.data["el"][self.element][3][row_num]
                                # Subtitle reorder button
                                rect = pygame.Rect(10, y + 6, 30, 30)
                                if rect.collidepoint(mouse_pos):
                                    self.reorder = row_num
                                y += 50
                            else:
                                x = 60
                                # Box select
                                for box_num in range(len(row)):
                                    rect = pygame.Rect(x, y, 40, 40)
                                    if rect.collidepoint(mouse_pos):
                                        self.switchEditor(["box", row_num, box_num])
                                    x += 50
                                # New box button
                                if len(row) < 5:
                                    rect = pygame.Rect(x, y + 10, 40, 40)
                                    if rect.collidepoint(mouse_pos):
                                        c.data["el"][self.element][3][row_num].append([None, 0])
                                        self.switchEditor(["box", row_num,
                                                           len(c.data["el"][self.element][3][row_num])-1])
                                # Delete button
                                rect = pygame.Rect(360, y + 17, 30, 30)
                                if rect.collidepoint(mouse_pos):
                                    del c.data["el"][self.element][3][row_num]
                                # Reorder button
                                rect = pygame.Rect(10, y + 17, 30, 30)
                                if rect.collidepoint(mouse_pos):
                                    self.reorder = row_num
                                y += 70

            else:
                # RIGHT SIDE
                # ---------------
                if self.edit is not None:
                    if self.edit[0] == "box":
                        if self.delete_box_button.click(event, mouse_pos):
                            del c.data["el"][self.element][3][self.edit[1]][self.edit[2]]
                            if len(c.data["el"][self.element][3][self.edit[1]]) == 0:
                                del c.data["el"][self.element][3][self.edit[1]]
                            self.edit = None
                        # Frames
                        positions = [(0, 0), (50, 0), (0, 50), (50, 50)]

                        for num in self.grid_images.keys():
                            pos = positions[num]
                            rect = pygame.Rect(c.width-240+pos[0],70+pos[1],40,40)
                            if rect.collidepoint(mouse_pos):
                                c.data["el"][self.element][3][self.edit[1]][self.edit[2]][1] = num
