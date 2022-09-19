import pygame
from scripts import common as c
from scripts.editor_objects.button import Button
from scripts.editor_objects.small_button import SmallButton
from scripts.editor_objects.text_input import TextInput
from scripts.menus.editor_sub.image_selection import ImageSelection
from scripts.utility.scale_image import scale_image
from scripts.utility.file_manager import get_file_list
from _thread import start_new_thread


class GridEditor:
    def __init__(self):
        self.element = c.selected[0]
        self.surf = pygame.Surface((c.width - 100, c.height - 100), pygame.SRCALPHA)
        self.sidebar = pygame.Surface((420, c.height - 100), pygame.SRCALPHA)

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
        self.frame_selection_indicator = pygame.image.load('assets/editor_gui/grid/arrow_down.png').convert_alpha()

        self.delete_box_button = SmallButton()
        self.title_text, self.box_preview = None, None
        self.image_selection = ImageSelection(size=(c.width - 600, c.height - 300))

        self.cached_images = {}
        self.create_rows()

    def create_rows(self):
        data = c.data["el"][self.element]
        self.sidebar = pygame.Surface((420, c.height - 100), pygame.SRCALPHA)
        self.sidebar.fill((45, 45, 50))
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
            self.sidebar.blit(self.reorder_bar, (50, reorder_y))

        x, y = 50, 50
        for row in data[3]:
            if len(row) > 0:
                if type(row[0]) == str:
                    self.sidebar.blit(self.title_row_img, (50, y))
                    text_surf = c.editor_font.render(row[0], True, (200, 200, 205))
                    self.sidebar.blit(text_surf, (60, y + 7))
                    # Bin button
                    self.sidebar.blit(self.bin_button, (360, y + 6))
                    # Reorder button
                    self.sidebar.blit(self.reorder_button, (10, y + 6))
                    y += 50
                else:
                    # Background
                    self.sidebar.blit(self.row_img, (50, y))
                    x = 60
                    # Boxes
                    for box in row:
                        self.sidebar.blit(self.grid_images[box[1]], (x, y + 10))
                        # Store images so they don't have to be loaded again
                        if box[0] is not None:
                            if box[0] in self.cached_images:
                                img = self.cached_images[box[0]]
                            else:
                                if box[0]+'.png' in get_file_list('projects/' + c.project_name + '/images/'):
                                    img = pygame.image.load(
                                        'projects/'+c.project_name+'/images/'+box[0]+'.png').convert_alpha()
                                    img = scale_image(img, 30)
                                    self.cached_images[box[0]] = img
                                else:
                                    img = None
                            if img is not None:
                                self.sidebar.blit(img, (x+5, y + 15))
                        x += 50
                    # New Box button
                    if len(row) < 5:
                        self.sidebar.blit(self.new_box_img, (x, y + 10))
                    # Bin button
                    self.sidebar.blit(self.bin_button, (360, y + 17))
                    # Reorder button
                    self.sidebar.blit(self.reorder_button, (10, y + 17))
                    y += 70
        self.new_row_button.render(self.sidebar, (50, y))
        self.new_title_button.render(self.sidebar, (205, y))

    def render(self):
        self.surf.fill((55, 55, 60))
        if self.reorder is not None:
            self.create_rows()
        self.surf.blit(self.sidebar, (0, 0))

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

                # Title input
                self.title_text.render(self.surf, (c.width - 290, 55))
                # Frame options
                x = c.width - 290
                for num in self.grid_images.keys():
                    self.surf.blit(self.grid_images[num], (x, 115))
                    x += 50
                # Frame selector
                selected = c.data["el"][self.element][3][self.edit[1]][self.edit[2]][1]
                self.surf.blit(self.frame_selection_indicator,(c.width-290+(50*selected),90))
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
            self.image_selection.image_clicked = None
            self.attemptPreviewLoad()
            print(data)
            self.title_text = TextInput(c.data["el"][self.element][3][self.edit[1]][self.edit[2]][2], None, width=140)

    def attemptPreviewLoad(self):
        image_name = c.data["el"][self.element][3][self.edit[1]][self.edit[2]][0]
        if image_name is None:
            self.need_preview = False
        else:
            image_name += ".png"
            if image_name in get_file_list('projects/' + c.project_name + '/images'):
                self.need_preview = False
                img = pygame.image.load('projects/' + c.project_name + '/images/'+image_name)
                self.box_preview = scale_image(img, 110)
                self.create_rows()
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
                if self.title_text.event(event, mouse_pos):
                    c.data["el"][self.element][3][self.edit[1]][self.edit[2]][2] = self.title_text.text
                output = self.image_selection.event(event, mouse_pos)
                if output is not None:
                    name, local = output[5] + output[0], output[4]
                    c.data["el"][self.element][3][self.edit[1]][self.edit[2]][0] = name
                    self.box_preview = scale_image(output[1], 110)
                    self.need_preview = True

        if event.type == pygame.VIDEORESIZE:
            self.surf = pygame.Surface((c.width - 100, c.height - 100))
            self.sidebar = pygame.Surface((420, c.height - 100), pygame.SRCALPHA)
            self.sidebar.fill((45, 45, 50))
            self.image_selection.resize((c.width - 600, c.height - 300))
            self.create_rows()

        if event.type == pygame.MOUSEBUTTONUP:
            if self.reorder is not None:
                data = c.data["el"][self.element][3]
                new_data = data.pop(self.reorder)
                if self.reorder_num > self.reorder:
                    self.reorder_num -= 1
                data.insert(self.reorder_num, new_data)
                self.reorder = None
                self.create_rows()
            self.reorder = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            # LEFT SIDE
            # ----------------

            if mouse_pos[0] < 420:
                if self.new_row_button.click(event, mouse_pos):
                    if len(c.data["el"][self.element][3]) == 0:
                        # Create a ticked box if there are not any rows yet
                        c.data["el"][self.element][3].append([[None, 1, ""]])
                    else:
                        c.data["el"][self.element][3].append([[None, 0, ""]])
                    self.create_rows()
                elif self.new_title_button.click(event, mouse_pos):
                    c.data["el"][self.element][3].append(["Subtitle"])
                    self.create_rows()

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
                                    self.create_rows()
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
                                        c.data["el"][self.element][3][row_num].append([None, 0, ""])
                                        self.switchEditor(["box", row_num,
                                                           len(c.data["el"][self.element][3][row_num]) - 1])
                                        self.create_rows()
                                # Delete button
                                rect = pygame.Rect(360, y + 17, 30, 30)
                                if rect.collidepoint(mouse_pos):
                                    self.edit = None
                                    del c.data["el"][self.element][3][row_num]
                                    self.create_rows()
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
                            self.create_rows()
                            if len(c.data["el"][self.element][3][self.edit[1]]) == 0:
                                del c.data["el"][self.element][3][self.edit[1]]
                                self.create_rows()
                            self.edit = None
                        # Frames

                        x = c.width - 290
                        for num in self.grid_images.keys():
                            rect = pygame.Rect(x, 115, 40, 40)
                            if rect.collidepoint(mouse_pos):
                                c.data["el"][self.element][3][self.edit[1]][self.edit[2]][1] = num
                                self.create_rows()
                                return
                            x += 50
