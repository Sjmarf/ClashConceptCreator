import pygame
from scripts import common as c
from scripts.editor_objects.button import Button
from scripts.editor_objects.small_button import SmallButton
from scripts.editor_objects.submenu_button import SubmenuButton
from scripts.editor_objects.file_input import FileInput
from scripts.editor_objects.text_input import TextInput
from scripts.editor_objects.choice_input import ChoiceInput
from scripts.editor_objects.colour_input import ColourInput

from scripts.utility import font
from scripts.menus.right_click import RightClick
from scripts.utility import element_actions


class SideBar:
    def __init__(self, size):
        self.surf, self.size = None, None
        self.prev_selected = None
        self.resize(size)
        self.title = font.FontObject("Background", "default", 20)
        self.elements, self.advanced_elements = [], []
        self.more_button = SmallButton(icon="more_button")
        self.advanced_button = Button("Advanced", width=150)
        self.hidden_button = Button("Hide", width=150)

        self.multi_select_elements = [(Button("Align X", width=150), "align_x"),
                                      (Button("Align Y", width=150), "align_y"),
                                      (Button("Space X", width=150), "space_x"),
                                      (Button("Space Y", width=150), "space_y")]
        self.advanced = False

        self.more_menu = RightClick()
        self.more_menu_shown = False

    def changeMenu(self):
        self.prev_selected = c.selected
        self.elements = []
        self.more_menu_shown = False

        if c.selected is not None:
            self.title.setText(c.selected[1].capitalize())
            data = c.data["el"][c.selected[0]]
            name, element = c.selected
            c.text_input_active = False

            if element == "background":
                self.elements = [FileInput(data[3], 'assets/backgrounds', ['background', 3],mode="background")]

            elif element == "menu":
                self.elements = [FileInput(data[3], 'assets/foregrounds', [c.selected[0], 3]),
                                 TextInput(data[4], [name, 4], label="Title"),
                                 TextInput(data[5], [name, 5],
                                           label="Font Size", int_only=True, int_min=10)]

            elif element == "button":
                self.elements = [FileInput(data[3], None, None, mode="button_type"),

                                 TextInput(data[4], [name, 4],
                                           label="Label", special_func="get_int_from_text"),

                                 TextInput(data[5], [name, 5],
                                           label="Font Size", int_only=True, int_min=10),

                                 ChoiceInput(data[6], [c.selected[0], 6], 'assets/elements/icon', label="Icon",
                                             window_width=200, allow_none=True, icon_size=30)]

                if data[3] == "custom":
                    self.elements.insert(1, ColourInput(data[7], [name, 7], label="Colour"))

            elif element == "grid":
                self.elements = [SubmenuButton("Edit Boxes", "grid", width=150),
                                 ChoiceInput(data[8], [name, 8],
                                             ["skin", "donation", "magic item"], mode="buttons", label="Type"),
                                 ChoiceInput(data[7], [name, 7],
                                             ["centre", "left"], mode="buttons", label="Align"),
                                 TextInput(str(data[4]), [name, 4],
                                           label="Font Size", int_only=True, int_min=10, convert_int=True),
                                 TextInput(str(data[6][0]), [name, 6, 0],
                                           label="Icon Pos x", int_only=True, convert_int=True),
                                 TextInput(str(data[6][1]), [name, 6, 1],
                                           label="Icon Pos y", int_only=True, convert_int=True),
                                 TextInput(str(data[5]), [name, 5],
                                           label="Icon Size", int_only=True, int_min=10, convert_int=True)
                                 ]

            elif element == "tabs":
                self.elements = [SubmenuButton("Edit Tabs", "tabs", width=150),
                                 ChoiceInput(data[5], [name, 5],
                                             ["1", "2"], mode="buttons", label="Type")]

            elif element == "text":
                self.elements = [TextInput(data[3], [name, 3], label="Text"),
                                 ColourInput(data[6], [name, 6], label="Text Colour"),
                                 ChoiceInput(data[5], [name, 5],
                                             ["left", "centre", "right"], mode="buttons", label="Align"),
                                 ChoiceInput(data[7], [name, 7],
                                             ["small", "large"], mode="buttons", label="Font"),
                                 TextInput(str(data[4]), [name, 4],
                                           label="Font Size", int_only=True, int_min=10, convert_int=True),
                                 ]

            elif element == "text block":
                self.elements = [SubmenuButton("Edit Text", "text_block", width=150),
                                 ColourInput(data[6], [name, 6], label="Text Colour"),
                                 ChoiceInput(data[5], [name, 5],
                                             ["left", "centre", "right"], mode="buttons", label="Align"),
                                 ChoiceInput(data[7], [name, 7],
                                             ["small", "large"], mode="buttons", label="Font"),
                                 TextInput(str(data[4]), [name, 4],
                                           label="Font Size", int_only=True, int_min=10, convert_int=True),
                                 ]

            elif element == "list":
                self.elements = [SubmenuButton("Edit Layout", "list_layout", width=150),
                                 SubmenuButton("Edit Entries", "list_entries", width=150),
                                 TextInput(str(data[6]), [name, 6],
                                           label="Icon Size", int_only=True, int_min=10, convert_int=True)]

            elif element == "image":
                self.elements = [SubmenuButton("Set Image", "image", width=150, path=[name, 3]),
                                 TextInput(str(data[4]), [name, 4],
                                           label="Image Size", int_only=True, int_min=10, convert_int=True)
                                 ]

            elif element == "chat":
                self.elements = [SubmenuButton("Messages", "chat", width=150)]

            elif element == "stat list":
                self.elements = [SubmenuButton("Edit", "stat list", width=150),
                                 ColourInput(data[4], [name, 4], label="Left"),
                                 ChoiceInput(data[6], [name, 6],
                                             ["small", "large"], mode="buttons"),
                                 TextInput(str(data[8]), [name, 8], int_only=True, int_min=10, convert_int=True),
                                 ColourInput(data[5], [name, 5], label="Right"),
                                 ChoiceInput(data[7], [name, 7],
                                             ["small", "large"], mode="buttons"),
                                 TextInput(str(data[9]), [name, 9], int_only=True, int_min=10, convert_int=True),
                                 ]

            elif element == "stat bars":
                self.elements = [SubmenuButton("Edit", "stat bars", width=150),
                                 ColourInput(data[4], [name, 4], label="Bar Colour"),
                                 TextInput(str(data[5]), [name, 5], int_only=True,
                                           int_min=28, convert_int=True, label="Bar Height")]

            elif element == "box":
                self.elements = [ChoiceInput(data[3], [name, 3],
                                             ["solid", "gradient", "map"],
                                             mode="buttons", label="Type")]
                if data[3] != "map":
                    self.elements.insert(1, ColourInput(data[4], [name, 4], label="Colour"))

            self.advanced_elements = [TextInput(str(data[0][0]), [name, 0, 0],
                                                label="Pos x", int_only=True, int_min=0, convert_int=True),
                                      TextInput(str(data[0][1]), [name, 0, 1],
                                                label="Pos y", int_only=True, int_min=0, convert_int=True),
                                      TextInput(str(data[1][0]), [name, 1, 0],
                                                label="Width", int_only=True, int_min=70, convert_int=True),
                                      TextInput(str(data[1][1]), [name, 1, 1],
                                                label="Height", int_only=True, int_min=55, convert_int=True)
                                      ]

    def render(self, main_pos):
        self.pos = main_pos
        if self.prev_selected != c.selected:
            self.changeMenu()

        self.surf.fill((50, 50, 55))

        if c.multi_select:
            if len(c.multi_select_elements) > 1:
                y = 70
                for element in self.multi_select_elements:
                    element[0].render(self.surf, (50, y))
                    y += 40

        else:
            if c.selected is not None:
                # Render delete button
                if c.selected[1] != "background":
                    self.more_button.render(self.surf, (self.size[0] - 45, 15))
                # Render Advanced button
                self.advanced_button.render(self.surf, (self.size[0] // 2 - 75, self.size[1] - 50))

                self.title.render(self.surf, (0, 13), centre=True)
                y = 70
                if self.advanced:
                    elements = self.advanced_elements
                    self.hidden_button.render(self.surf, (self.size[0] // 2 - 75, 400))
                else:
                    elements = self.elements
                for element in elements:
                    element.render(self.surf, (0, y), centre=True)
                    y += element.HEIGHT + 20

        c.display.blit(self.surf, main_pos)
        if self.more_menu_shown and c.selected is not None:
            self.more_menu.render(c.display, (main_pos[0] + 25, 60))

    def event(self, event):
        pos = (0, 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - self.pos[0], event.pos[1] - self.pos[1])

            if self.more_menu_shown and c.selected is not None:
                output = self.more_menu.event(event)
                if type(output) == str:
                    if output == "delete":
                        element_actions.delete()
                    elif output == "duplicate":
                        element_actions.duplicate()
                    elif output == "move up layer":
                        element_actions.layer_up()
                    elif output == "move down layer":
                        element_actions.layer_down()
                    self.more_menu_shown = False

        if c.selected is not None and not c.multi_select:
            if self.advanced_button.click(event, pos):
                self.advanced = not self.advanced
                self.changeMenu()

            if c.selected[1] != "background":
                if self.more_button.click(event, pos):
                    self.more_menu_shown = not self.more_menu_shown
                    self.more_menu.set_options(["move up layer", "move down layer", "duplicate", "delete"])

            if not self.more_menu_shown:
                if self.advanced:
                    if self.hidden_button.click(event, pos):
                        if c.selected[0] in c.data["hidden"]:
                            c.data["hidden"].remove(c.selected[0])
                        else:
                            c.data["hidden"].append(c.selected[0])
                        c.menu.canvas.draw()
                    elements = self.advanced_elements
                else:
                    elements = self.elements
                for element in elements:
                    element.event(event, pos)

        if c.multi_select:
            if len(c.multi_select_elements) > 1:
                for element in self.multi_select_elements:
                    if element[0].click(event, pos):

                        if element[1] == "align_x":
                            avg = 0
                            for el in c.multi_select_elements:
                                avg += c.data["el"][el][0][0]
                            avg /= len(c.multi_select_elements)
                            for el in c.multi_select_elements:
                                c.data["el"][el][0][0] = avg
                            c.menu.canvas.draw()

                        elif element[1] == "align_y":
                            avg = 0
                            for el in c.multi_select_elements:
                                avg += c.data["el"][el][0][1]
                            avg /= len(c.multi_select_elements)
                            for el in c.multi_select_elements:
                                c.data["el"][el][0][1] = avg
                            c.menu.canvas.draw()

                        elif element[1] == "space_x":
                            avg = 0
                            prev = None
                            # Get average spacing between elements
                            for el in c.multi_select_elements[:-1]:
                                if prev is None:
                                    prev = c.data["el"][el][1][0]+c.data["el"][el][0][0]
                                else:
                                    avg += c.data["el"][el][0][0] - prev
                                    prev = c.data["el"][el][1][0]+c.data["el"][el][0][0]
                            avg /= len(c.multi_select_elements)-1

                            start_pos = c.data["el"][c.multi_select_elements[0]][0][0]
                            prev_width = 0
                            for el in c.multi_select_elements:
                                c.data["el"][el][0][0] = start_pos + prev_width
                                prev_width += c.data["el"][el][1][0] + avg

                            c.menu.canvas.draw()

                        elif element[1] == "space_y":
                            avg = 0
                            prev = None
                            # Get average spacing between elements
                            for el in c.multi_select_elements:
                                if prev is None:
                                    prev = c.data["el"][el][1][1]+c.data["el"][el][0][1]
                                else:
                                    avg += c.data["el"][el][0][1] - prev
                                    prev = c.data["el"][el][1][1]+c.data["el"][el][0][1]
                            avg /= len(c.multi_select_elements)-1

                            start_pos = c.data["el"][c.multi_select_elements[0]][0][1]
                            prev_width = 0
                            for el in c.multi_select_elements:
                                c.data["el"][el][0][1] = start_pos + prev_width
                                prev_width += c.data["el"][el][1][1] + avg

                            c.menu.canvas.draw()

    def resize(self, size):
        self.surf = pygame.Surface(size, pygame.SRCALPHA)
        self.size = size
