import pygame
from scripts import common as c
from scripts.utility.font import FontObject
from scripts.utility.size_element import size_element


def getIntFromText(path):
    # Used to set button element width to that required by text
    new_width = len(c.data["el"][path[0]][path[1]]) * 13 + 30
    old_width = c.data["el"][path[0]][1]
    if old_width[0] < new_width:
        c.data["el"][path[0]][1] = [new_width, old_width[1]]
        c.menu.side_bar.changeMenu()


class TextInput:
    def __init__(self, text, path, label=None, width=150, empty=None, int_only=False,
                 int_min=None, special_func=None, convert_int=False, no_editor=False):
        self.path = path
        self.img, self.pos, self.text, self.empty, self.label = None, (0, 0), text, empty, label
        self.active, self.no_editor = False, no_editor
        self.int_only, self.int_min, self.function, self.convert_int = int_only, int_min, None, convert_int

        if special_func is not None:
            if special_func == "get_int_from_text":
                self.function = getIntFromText
        if label is not None:
            self.HEIGHT = 60
            self.label_img = c.editor_font.render(label, True, (200, 200, 205))
        else:
            self.HEIGHT = 30
            self.label_img = None

        self.width = width
        self.img = size_element('assets/editor_gui/text_input.png',(width,30),edge=(5,5,5,5))
        self.highlight = size_element('assets/editor_gui/text_input_highlight.png',(width,30),edge=(5,5,5,5))
        self.fade = pygame.image.load('assets/editor_gui/text_fade.png').convert_alpha()
        self.renderText()
        self.backspace_tick = 35

    def render(self, surf, pos, centre=False):
        if self.active:
            img = self.highlight
        else:
            img = self.img
        if centre:
            self.pos = (surf.get_width() // 2 - 75, pos[1])
        else:
            self.pos = pos

        if self.label_img is not None:
            surf.blit(self.label_img, self.pos)
            self.pos = (self.pos[0], self.pos[1] + 30)
        surf.blit(img, self.pos)
        surf.blit(self.text_img, (self.pos[0] + 5, self.pos[1] + 1))

        if self.active:
            if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                self.backspace_tick -= 60/c.fps
                if self.backspace_tick < 0:
                    self.backspace_tick = 5
                    self.text = self.text[:-1]
                    self.renderText()
            else:
                self.backspace_tick = 35

    def event(self, event, pos) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rect = pygame.Rect((self.pos[0], self.pos[1], self.width, 30))
                if rect.collidepoint(pos):

                    self.active = not self.active
                    c.text_input_active = self.active
                    self.renderText()
                    if not self.active:
                        if not self.no_editor:
                            c.menu.canvas.draw()
                        return True

                elif self.active:
                    self.active, c.text_input_active = False, False
                    if not self.no_editor:
                        c.menu.canvas.draw()
                    self.renderText()
                    return True
        elif event.type == pygame.KEYDOWN and self.active:

            if event.key in {pygame.K_ESCAPE, pygame.K_RETURN}:
                self.active, c.text_input_active = False, False
                # Check if input value is below minimum
                if self.int_min is not None:
                    if self.text == "":
                        self.text = str(self.int_min)
                    elif int(self.text) < self.int_min:
                        self.text = str(self.int_min)
                # Run special func if included
                if self.function is not None:
                    self.function(self.path)
                self.renderText()
                if not self.no_editor:
                    c.menu.canvas.draw()
                return True

            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.renderText()

            elif pygame.key.get_mods() in {64,1024} and event.key == pygame.K_v:
                data = pygame.scrap.get("text/plain;charset=utf-8")
                if data is not None:
                    data = data.decode("utf-8")
                    self.text += data
                    self.renderText()

            elif event.unicode in "0123456789.-" or not self.int_only:
                self.text += event.unicode
                self.renderText()

    def renderText(self):
        self.text_img = pygame.Surface((self.width-10, 30), pygame.SRCALPHA)
        if self.text == "" and self.empty is not None:
            text_img = c.editor_font.render(self.empty, True, (100, 100, 105))
        else:
            text_img = c.editor_font.render(self.text, True, (200, 200, 205))

        if self.active:
            xpos = min(0, self.width-10 - text_img.get_width())
            self.text_img.blit(text_img, (xpos, 0))
        else:
            self.text_img.blit(text_img, (0, 0))
            self.text_img.blit(self.fade, (self.width-40, 0), special_flags=pygame.BLEND_RGBA_SUB)

        data = self.text
        if self.convert_int:
            if data == '':
                data = 0
            else:
                if "-" in data:
                    data = data.replace("-", "")
                    if data == "":
                        data = 0
                    data = int(float(data)) * -1
                else:
                    data = int(float(data))
        if self.path is not None:
            if len(self.path) == 2:
                c.data["el"][self.path[0]][self.path[1]] = data
            else:
                # print(c.data["el"][self.path[0]][self.path[1]])
                c.data["el"][self.path[0]][self.path[1]][self.path[2]] = data
