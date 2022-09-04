import pygame
from scripts import common as c
from scripts.menus.menus.main_menu import MainMenu
from scripts.utility.file_manager import load_json
import ctypes

pygame.init()

import platform
if platform.system() == "Darwin":
    pygame.display.set_icon(pygame.image.load('assets/app icons/mac.png'))
else:
    pygame.display.set_icon(pygame.image.load('assets/app icons/windows.png'))
del platform

pygame.font.init()
c.editor_font = pygame.font.Font("assets/fonts/Verdana.ttf", 20)
c.editor_font_large = pygame.font.Font("assets/fonts/Verdana.ttf", 30)
c.editor_font_small = pygame.font.Font("assets/fonts/Verdana.ttf", 15)

c.DISCORD_LINK = "https://discord.gg/Q4rwc3MVBq"

c.fps = 60
c.display = pygame.display.set_mode((900, 600), pygame.RESIZABLE)
pygame.display.set_caption('Clash Concept Creator')

pygame.scrap.init()

c.width, c.height = 900, 600
c.clock = pygame.time.Clock()
c.settings = load_json('data/settings.json')

# You can use the in-game 'version number' option in settings to update the version number everywhere, automatically.
c.VERSION = c.settings["version"]

c.menu = MainMenu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if type(c.menu).__name__ == "Editor":
                if c.unsaved_changes:
                    from scripts.menus.editor_sub.quit_confirm import QuitConfirm

                    c.submenu = QuitConfirm(quit_window=True)
                    break
            pygame.quit()
            raise SystemExit(0)
        if event.type == pygame.VIDEORESIZE:
            c.display = pygame.display.set_mode((max(800, event.w), max(450, event.h)), pygame.RESIZABLE)
            c.width, c.height = c.display.get_size()
        c.menu.event(event)

    c.menu.render()
    c.clock.tick(60)
    c.fps = int(c.clock.get_fps())
    pygame.display.flip()
