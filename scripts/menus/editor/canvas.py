import pygame
import time
from scripts import common as c
from _thread import start_new_thread
from scripts.utility import element_actions

from scripts.elements.button import renderButton
from scripts.elements.grid import renderGrid
from scripts.elements.image import renderImage
from scripts.elements.text import renderTextEl
from scripts.elements.text_block import renderTextBlock
from scripts.elements.tabs import renderTabs
from scripts.elements.box import renderBox
from scripts.elements.list import renderList
from scripts.elements.chat import renderChat
from scripts.elements.menu import renderMenu
from scripts.elements.stat_list import renderStatList
from scripts.elements.stat_bars import renderStatBars


class Canvas:
    def __init__(self, size):
        self.zoom = 1
        self.pos = [0,0]
        self.snap_lines = {"x": [667], "y": [375]}
        c.canvas = pygame.Surface(c.canvas_size, pygame.SRCALPHA)
        c.canvas.fill((20, 20, 25))
        self.draw(check_for_changes=False)
        c.changed_since_opened = False
        self.size, self.scale_factor = size, 1
        self.transform, self.selection_size, self.selection_pos = None, (0, 0), (0, 0)
        self.node_img = pygame.image.load('assets/editor_gui/node.png').convert_alpha()

    def draw(self, check_for_changes=True):
        c.changed_since_opened = True
        if check_for_changes:
            c.menu.check_for_changes()
        start_new_thread(self.drawThread, ())

    def drawThread(self):
        start_time = time.time()
        c.images_used = []
        # Used to calculate what image should be used for project icon.
        c.icon_image = (None, 0)  # (Image_name, image area)
        canvas = pygame.Surface(c.canvas_size, pygame.SRCALPHA)
        element_layer = pygame.Surface(canvas.get_size(), pygame.SRCALPHA)
        # Load foreground
        # img = pygame.image.load('assets/foregrounds/' + c.data["el"]["foreground"][3] + '.png').convert_alpha()
        # c.canvas.blit(img, (0, 0))
        # Load elements
        data = c.data["el"].copy()
        self.snap_lines = {"x": [667], "y": [375]}

        draw_funcs = {"background": None,
                      "button": renderButton,
                      "grid": renderGrid,
                      "image": renderImage,
                      "text": renderTextEl,
                      "box": renderBox,
                      "menu": renderMenu,
                      "text block": renderTextBlock,
                      "tabs": renderTabs,
                      "list": renderList,
                      "chat": renderChat,
                      "stat list": renderStatList,
                      "stat bars": renderStatBars}

        draw_dark = False
        for element in range(len(data)):
            el_start_time = time.time()
            if element not in c.data["hidden"]:
                pos, size, name = data[element][0:3]
                func = draw_funcs[name]
                if name == "menu":
                    # Darken the background image
                    draw_dark = True

                if name == "background":
                    if c.data["el"][element][3] is not None:
                        img = c.image_store.get_background('assets/backgrounds/' + c.data["el"][element][3] + '.png')
                        canvas.blit(img, (0, 0))
                else:
                    img = func(element)
                    if c.multi_select and img is not None:
                        if element not in c.multi_select_elements:
                            # Darken image for multi-select
                            col_surf = pygame.Surface(size)
                            col_surf.fill((90, 90, 90))
                            img.blit(col_surf, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                    if img is not None:
                        element_layer.blit(img, pos)

                if not pos[0] + size[0] in self.snap_lines['x']:
                    self.snap_lines['x'].append(pos[0] + size[0] // 2)
                if not pos[1] + size[1] in self.snap_lines['y']:
                    self.snap_lines['y'].append(pos[1] + size[1] // 2)
            # print("element "+data[element][2], round(time.time() - el_start_time,3))
        # print("TOTAL TIME: ",round(time.time()-start_time,3))
        c.image_store.clear_unused_images()
        if draw_dark and c.data["el"][0][3] is not None:
            dark_img = pygame.Surface(c.canvas.get_size(), pygame.SRCALPHA)
            dark_img.fill((0, 0, 0, 120))
            canvas.blit(dark_img, (0, 0))
        canvas.blit(element_layer, (0, 0))
        c.canvas = canvas

    def render(self):
        self.scale_factor = self.size[0] / c.canvas.get_width()
        canvas = pygame.transform.smoothscale(c.canvas, (self.size[0] * self.zoom, self.size[1] * self.zoom))
        abs_pos = pygame.mouse.get_pos()
        sf = self.scale_factor
        offset = (self.selection_size[0] // 2, self.selection_size[1] // 2)
        real_pos = (abs_pos[0] // sf - offset[0], abs_pos[1] // sf - offset[1])

        # Calculate object movement
        if self.transform == "move":
            # Snap lines
            if pygame.key.get_pressed()[pygame.K_y] or pygame.key.get_pressed()[pygame.K_LSHIFT]:
                # X
                closest = min(self.snap_lines["x"], key=lambda x: abs(x - real_pos[0] - self.selection_size[0] // 2))
                if real_pos[0] - closest + self.selection_size[0] // 2 in range(-50, 50):
                    real_pos = (closest - self.selection_size[0] // 2, real_pos[1])
            if pygame.key.get_pressed()[pygame.K_x] or pygame.key.get_pressed()[pygame.K_LSHIFT]:
                # Y
                closest = min(self.snap_lines["y"], key=lambda y: abs(y - real_pos[1] - self.selection_size[1] // 2))
                if real_pos[1] - closest + self.selection_size[1] // 2 in range(-50, 50):
                    real_pos = (real_pos[0], closest - self.selection_size[1] // 2)

            abs_pos = (real_pos[0] * sf, real_pos[1] * sf)
            # Update saved value
            c.data["el"][c.selected[0]][0] = [int(real_pos[0]), int(real_pos[1])]

            # Draw snap lines
            if pygame.key.get_pressed()[pygame.K_y] or pygame.key.get_pressed()[pygame.K_LSHIFT]:
                for line in self.snap_lines["x"]:
                    pygame.draw.line(canvas, (255, 0, 0), (line * self.scale_factor, 0),
                                     (line * self.scale_factor, c.canvas_size[1]))
            if pygame.key.get_pressed()[pygame.K_x] or pygame.key.get_pressed()[pygame.K_LSHIFT]:
                for line in self.snap_lines["y"]:
                    pygame.draw.line(canvas, (0, 0, 255), (0, line * self.scale_factor),
                                     (c.canvas_size[0], line * self.scale_factor))

        # DRAW BOXES
        if c.selected is not None:
            if c.selected[1] != "background":
                # Original size and position of the object
                pos = c.data["el"][c.selected[0]][0]
                pos = (pos[0] * sf * self.zoom, pos[1] * sf * self.zoom)
                size = (self.selection_size[0] * sf * self.zoom, self.selection_size[1] * sf * self.zoom)
                # Draw red outline when moving object
                if self.transform is not None:
                    if self.transform == "move":
                        pygame.draw.rect(canvas, (200, 0, 0),
                                         (abs_pos[0], abs_pos[1],
                                          self.selection_size[0] * sf * self.zoom,
                                          self.selection_size[1] * sf * self.zoom), 2)

                    elif 'resize' in self.transform:
                        borders = [pos[0], pos[1], size[0], size[1]]
                        if 'right' in self.transform:
                            borders[2] = abs_pos[0] - pos[0]

                        elif 'left' in self.transform:
                            borders[0] = abs_pos[0]
                            borders[2] = size[0] + pos[0] - abs_pos[0]

                        if 'bottom' in self.transform:
                            borders[3] = abs_pos[1] - pos[1]

                        elif 'top' in self.transform:
                            borders[1] = abs_pos[1]
                            borders[3] = size[1] + pos[1] - abs_pos[1]

                        pygame.draw.rect(canvas, (200, 0, 0),
                                         borders, 2)

                else:
                    # Draw box and handles
                    pygame.draw.rect(canvas, (200, 0, 0), (pos[0], pos[1], size[0], size[1]), 2)
                    # Handles
                    canvas.blit(self.node_img, (pos[0] + size[0] // 2 - 6, pos[1] + size[1] // 2 - 6))  # Centre
                    canvas.blit(self.node_img, (pos[0] - 6, pos[1] + size[1] // 2 - 6))  # Left
                    canvas.blit(self.node_img, (pos[0] + size[0] - 6, pos[1] + size[1] // 2 - 6))  # Right
                    canvas.blit(self.node_img, (pos[0] + size[0] // 2 - 6, pos[1] - 6))  # Top
                    canvas.blit(self.node_img, (pos[0] + size[0] // 2 - 6, pos[1] + size[1] - 6))  # Bottom
                    canvas.blit(self.node_img, (pos[0] - 6, pos[1] - 6))  # Top-Left
                    canvas.blit(self.node_img, (pos[0] + size[0] - 6, pos[1] - 6))  # Top-Right
                    canvas.blit(self.node_img, (pos[0] - 6, pos[1] + size[1] - 6))  # Bottom-Left
                    canvas.blit(self.node_img, (pos[0] + size[0] - 6, pos[1] + size[1] - 6))  # Bottom-Right

        cropped_canvas = pygame.Surface(self.size, pygame.SRCALPHA)
        cropped_canvas.blit(canvas, self.pos) #(cropped_canvas.get_width() // 2 - canvas.get_width() // 2,
                                     #cropped_canvas.get_height() // 2 - canvas.get_height() // 2)
        c.display.blit(cropped_canvas, (0, 0))

    def event(self, event):
        #if event.type == pygame.MOUSEWHEEL:
            #self.pos[0] -= event.x*5
            ##self.pos[1] += event.y*5

        if event.type == pygame.KEYDOWN:
            if c.multi_select:
                if pygame.key.get_mods():
                    amount = 5
                else:
                    amount = 1
                if event.key == pygame.K_LEFT:
                    for item in c.multi_select_elements:
                        c.data["el"][item][0][0] -= amount
                elif event.key == pygame.K_RIGHT:
                    for item in c.multi_select_elements:
                        c.data["el"][item][0][0] += amount
                elif event.key == pygame.K_UP:
                    for item in c.multi_select_elements:
                        c.data["el"][item][0][1] -= amount
                elif event.key == pygame.K_DOWN:
                    for item in c.multi_select_elements:
                        c.data["el"][item][0][1] += amount
                self.draw()
            else:
                if c.selected is not None:
                    if c.selected[1] not in {"menu", "background"}:
                        pos = (0, 0)
                        if event.key == pygame.K_LEFT:
                            pos = (-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            pos = (1, 0)
                        elif event.key == pygame.K_UP:
                            pos = (0, -1)
                        elif event.key == pygame.K_DOWN:
                            pos = (0, 1)
                        if pygame.key.get_mods():
                            pos = (pos[0] * 5, pos[1] * 5)
                        if pos != (0, 0):
                            old_pos = c.data["el"][c.selected[0]][0]
                            c.data["el"][c.selected[0]][0] = [old_pos[0] + pos[0], old_pos[1] + pos[1]]
                            self.draw()
                            c.menu.side_bar.changeMenu()

                    if c.selected[1] != "background" and not c.text_input_active and self.transform is None:
                        keys = pygame.key.get_pressed()
                        if event.key == pygame.K_PERIOD:
                            element_actions.layer_up()
                        elif event.key == pygame.K_COMMA:
                            element_actions.layer_down()
                        elif event.key == pygame.K_d and keys[pygame.K_LSHIFT]:
                            element_actions.duplicate()
                        elif event.key == pygame.K_x:
                            element_actions.delete()
                        elif event.key == pygame.K_m:
                            self.transform = "move"

                #if event.key == pygame.K_EQUALS:
                    #self.zoom += 0.1
                    #self.pos[0] -= 1334 * 0.025
                    #self.pos[1] -= 750 * 0.025
                #elif event.key == pygame.K_MINUS:
                    #self.zoom -= 0.1
                    #self.pos[0] += 1334 * 0.025
                    #self.pos[1] += 750 * 0.025

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.transform is not None:
                    self.post_transform()
                else:
                    sf = self.scale_factor
                    if event.pos[0] < self.size[0] and event.pos[1] < self.size[1]:
                        # Foreground and background
                        select, sel_size, sel_pos = [0, "background"], (70, 60), (0, 0)

                        # Elements
                        for num, data in enumerate(c.data["el"]):
                            if data[2] != "background":
                                if c.selected is not None:
                                    # Allows you to click multiple times if an element is behind
                                    # if c.selected[0] == num:
                                    # break
                                    pass
                                size = data[1]
                                rect = pygame.Rect(data[0][0] * sf, data[0][1] * sf, size[0] * sf,
                                                   size[1] * sf)
                                if rect.collidepoint(event.pos):
                                    select = [num, data[2]]
                                    sel_size, sel_pos = size, data[0]
                                    self.transform = None

                        # Selected element handles
                        if c.selected is not None:
                            if c.selected[0] != "background":
                                pos = (
                                    self.selection_pos[0] * self.scale_factor * self.zoom + self.pos[0],
                                    self.selection_pos[1] * self.scale_factor * self.zoom + self.pos[1])
                                size = (
                                    self.selection_size[0] * self.scale_factor * self.zoom,
                                    self.selection_size[1] * self.scale_factor * self.zoom)
                                # Centre
                                rect = pygame.Rect(pos[0] + size[0] // 2 - 6, pos[1] + size[1] // 2 - 6, 12, 12)
                                if rect.collidepoint(event.pos):
                                    print('move')
                                    self.transform = "move"
                                # Right
                                rect = pygame.Rect(pos[0] + size[0] - 6, pos[1] + size[1] // 2 - 6, 12, 12)
                                if rect.collidepoint(event.pos):
                                    self.transform = "resize-right"
                                # Left
                                rect = pygame.Rect(pos[0] - 6, pos[1] + size[1] // 2 - 6, 12, 12)
                                if rect.collidepoint(event.pos):
                                    self.transform = "resize-left"
                                # Top
                                rect = pygame.Rect(pos[0] + size[0] // 2 - 6, pos[1] - 6, 12, 12)
                                if rect.collidepoint(event.pos):
                                    self.transform = "resize-top"
                                # Bottom
                                rect = pygame.Rect(pos[0] + size[0] // 2 - 6, pos[1] + size[1] - 6, 12, 12)
                                if rect.collidepoint(event.pos):
                                    self.transform = "resize-bottom"
                                # Top-Left
                                rect = pygame.Rect(pos[0] - 6, pos[1] - 6, 12, 12)
                                if rect.collidepoint(event.pos):
                                    self.transform = "resize-top-left"
                                # Top-Right
                                rect = pygame.Rect(pos[0] - 6 + size[0], pos[1] - 6, 12, 12)
                                if rect.collidepoint(event.pos):
                                    self.transform = "resize-top-right"
                                # Bottom-Left
                                rect = pygame.Rect(pos[0] - 6, pos[1] + size[1] - 6, 12, 12)
                                if rect.collidepoint(event.pos):
                                    self.transform = "resize-bottom-left"
                                # Bottom-Right
                                rect = pygame.Rect(pos[0] + size[0] - 6, pos[1] + size[1] - 6, 12, 12)
                                if rect.collidepoint(event.pos):
                                    self.transform = "resize-bottom-right"

                                if self.transform is not None:
                                    # Cancel the selection-switching code if a handle is clicked.
                                    select, sel_size, sel_pos = c.selected, self.selection_size, self.selection_pos

                        if c.multi_select:
                            if select[0] in c.multi_select_elements:
                                c.multi_select_elements.remove(select[0])
                            else:
                                c.multi_select_elements.append(select[0])
                            self.draw()
                        else:
                            c.selected, self.selection_size, self.selection_pos = select, sel_size, sel_pos
                        # Move selected element to top of dict
                        # old = c.data["el"].pop(c.selected[0])
                        # c.data["el"][c.selected[0]] = old

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.transform is not None:
                    self.post_transform()

    def post_transform(self):
        min_size = (70, 55)
        if c.selected is not None:
            if c.selected[1] in {"text block", "text"}:
                min_size = (5, 5)

        if self.transform is not None:
            abs_pos = pygame.mouse.get_pos()
            old_size = c.data["el"][c.selected[0]][1]
            new_size = old_size.copy()
            pos = c.data["el"][c.selected[0]][0]
            new_pos = pos.copy()

            if 'resize' in self.transform:
                if 'right' in self.transform:
                    new_size[0] = max(min_size[0], int(abs_pos[0] // self.scale_factor - pos[0]))

                elif 'left' in self.transform:
                    new_pos[0] = abs_pos[0] // self.scale_factor
                    new_size[0] = max(min_size[0], int(pos[0] - (abs_pos[0] // self.scale_factor)
                                                       + c.data["el"][c.selected[0]][1][0]))

                if 'bottom' in self.transform:
                    new_size[1] = max(min_size[1], int(abs_pos[1] // self.scale_factor - pos[1]))

                elif 'top' in self.transform:
                    new_pos[1] = abs_pos[1] // self.scale_factor
                    new_size[1] = max(min_size[1], int(pos[1] - (abs_pos[1] // self.scale_factor)
                                                       + c.data["el"][c.selected[0]][1][1]))

            c.data["el"][c.selected[0]][1] = new_size
            c.data["el"][c.selected[0]][0] = new_pos

            self.selection_pos = c.data["el"][c.selected[0]][0]
            self.selection_size = c.data["el"][c.selected[0]][1]

            self.transform = None
            self.draw()
            if c.menu.side_bar.advanced:
                c.menu.side_bar.changeMenu()
