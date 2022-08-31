import pygame
from scripts import common as c
from scripts.editor_objects.text_input import TextInput
from scripts.editor_objects.choice_input import ChoiceInput
from scripts.editor_objects.button import Button


class TabEditor:
    def __init__(self):
        self.element = c.selected[0]
        self.data = c.data["el"][self.element][3]
        self.selected = c.data["el"][self.element][4]
        self.mode = c.data["el"][self.element][5]
        self.row_inputs = []
        self.reloaded = False
        self.loadRows()

        self.surf = pygame.Surface((260, 430), pygame.SRCALPHA)
        self.bin_button = pygame.image.load('assets/editor_gui/bin_button.png').convert_alpha()
        self.checkbox_1 = pygame.image.load('assets/editor_gui/checkbox1.png').convert_alpha()
        self.checkbox_2 = pygame.image.load('assets/editor_gui/checkbox2.png').convert_alpha()
        self.done_button = Button("Done", width=150)
        self.add_button = Button("+", width=150)

    def loadRows(self):
        self.row_inputs = []
        for num, item in enumerate(self.data):
            if c.data["el"][self.element][5] == "2":
                self.row_inputs.append(ChoiceInput(item, [c.selected[0], 3, num], 'assets/elements/icon',
                                                   window_width=200, allow_none=True, submenu_layer=2, icon_size=30))
            else:
                self.row_inputs.append(TextInput(item, None))

    def render(self):
        self.surf.fill((50, 50, 55))
        y = 15
        for num, item in enumerate(self.row_inputs):
            item.render(self.surf, (55, y))
            self.surf.blit(self.bin_button, (215, y))

            if self.selected == num:
                self.surf.blit(self.checkbox_2, (15, y))
            else:
                self.surf.blit(self.checkbox_1, (15, y))
            y += 40

        if len(self.row_inputs) < 9:
            self.add_button.render(self.surf, (55, y))

        self.done_button.render(self.surf, (55, 390))

        c.display.blit(self.surf, (c.width // 2 - 130, c.height // 2 - 200))

        # Detect when icon picker is closed and reload
        if c.submenu2 is None and not self.reloaded:
            self.reloaded = True
            self.loadRows()
        elif c.submenu2 is not None:
            self.reloaded = False

    def event(self, event):
        pos = (0, 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - (c.width // 2 - 130), event.pos[1] - (c.height // 2 - 200))

        y = 15
        for num, item in enumerate(self.row_inputs):
            if item.event(event, pos) and self.mode == "1":
                self.data[num] = item.text

            if event.type == pygame.MOUSEBUTTONDOWN:
                bin_rect = pygame.Rect((215, y, 30, 30))
                if bin_rect.collidepoint(pos):
                    del self.data[num]
                    self.loadRows()
                    break
                select_rect = pygame.Rect((15, y, 30, 30))
                if select_rect.collidepoint(pos):
                    self.selected, c.data["el"][self.element][4] = num, num
            y += 40

        if len(self.row_inputs) < 9:
            if self.add_button.click(event, pos):
                self.data.append("")
                self.loadRows()

        if self.done_button.click(event, pos):
            c.submenu = None
            c.menu.canvas.draw()
