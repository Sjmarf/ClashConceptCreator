import pygame
from scripts import common as c

from scripts.menus.base_designer.board import Board
from scripts.menus.base_designer.scenery import Scenery
from scripts.menus.base_designer.bottom_bar import BottomBar

from scripts.utility.image_store import ImageStore



class BaseDesigner:
    def __init__(self):
        print("Base Designer initialised")
        c.selected = None
        self.view = "board"
        c.canvas_size = [1334, 750]
        # Submenu2 is used for popups inside of submenus
        c.submenu = None

        self.blackout = pygame.Surface(c.display.get_size(), pygame.SRCALPHA)
        self.blackout.fill((0, 0, 0, 180))

        c.image_store = ImageStore()

        self.board = Board()
        self.scenery = Scenery()
        self.bottom_bar = BottomBar()

    def render(self):
        c.display.fill((0, 0, 0))
        if self.view == "board":
            self.board.render()
        else:
            self.scenery.render()
        self.bottom_bar.render()

        if c.submenu is not None:
            self.blackout.set_alpha(180)
            c.display.blit(self.blackout, (0, 0))
            c.submenu.render()

    def event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.blackout = pygame.Surface(c.display.get_size(), pygame.SRCALPHA)
            self.blackout.fill((0, 0, 0, 180))

        if c.submenu is not None:
            c.submenu.event(event)

        else:
            if self.view == "board":
                self.board.event(event)
            else:
                self.scenery.event(event)
            self.bottom_bar.event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if self.view == "board":
                    self.view = "scenery"
                    self.scenery.draw()
                else:
                    self.view = "board"
