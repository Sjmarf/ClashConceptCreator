from scripts import common as c
from scripts.utility.spritesheet import SpriteSheet
import pygame


class SubmenuButton:
    def __init__(self, text, submenu, width=None, path=None):
        text = c.editor_font.render(text, True, (200, 200, 200))
        if width is None:
            width = text.get_width() + 30

        src = pygame.image.load('assets/editor_gui/button.png').convert_alpha()
        sheet = SpriteSheet(src, direct=True)
        img = pygame.Surface((width, 30), pygame.SRCALPHA)
        self.HEIGHT = 30

        mid = pygame.transform.scale(sheet.image((30, 0, 50, 30)), (width - 60, 30))
        img.blit(mid, (30, 0))
        img.blit(sheet.image((0, 0, 30, 30)), (0, 0))
        img.blit(sheet.image((80, 0, 30, 30)), (width - 30, 0))
        img.blit(text, (width // 2 - text.get_width() // 2, 1))
        self.img = img
        self.pos = (-1000, 0)
        self.submenu, self.path, self.width = submenu, path, width
        # self.img = pygame.transform.smoothscale(img,(img.get_width()//2,30))

    def render(self, surf, pos, centre=False):
        if centre:
            pos = (surf.get_width() // 2 - self.img.get_width() // 2, pos[1])
        self.pos = pos
        surf.blit(self.img, pos)

    def event(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rect = pygame.Rect(self.pos[0], self.pos[1], self.width, 30)
                if rect.collidepoint(pos):
                    if self.submenu is not None:
                        if self.submenu == "grid":
                            from scripts.menus.editor_sub.grid_editor import GridEditor
                            c.submenu = GridEditor()
                        elif self.submenu == "image":
                            from scripts.menus.editor_sub.image_selection import ImageWindow
                            c.submenu = ImageWindow(self.path)
                        elif self.submenu == "text_block":
                            from scripts.menus.editor_sub.text_input_menu import TextInputMenu
                            c.submenu = TextInputMenu()
                        elif self.submenu == "tabs":
                            from scripts.menus.editor_sub.tab_editor import TabEditor
                            c.submenu = TabEditor()
                        elif self.submenu == "list_layout":
                            from scripts.menus.editor_sub.list_layout_editor import ListLayoutEditor
                            c.submenu = ListLayoutEditor()
                        elif self.submenu == "list_entries":
                            from scripts.menus.editor_sub.list_entries_editor import ListEntriesEditor
                            c.submenu = ListEntriesEditor()
                        elif self.submenu == "chat":
                            from scripts.menus.editor_sub.chat_editor import ChatEditor
                            c.submenu = ChatEditor()
                        elif self.submenu == "stat list":
                            from scripts.menus.editor_sub.stat_list import StatListEditor
                            c.submenu = StatListEditor()
                        elif self.submenu == "bars":
                            from scripts.menus.editor_sub.stat_bars import BarsEditor
                            c.submenu = BarsEditor()
                    return True
