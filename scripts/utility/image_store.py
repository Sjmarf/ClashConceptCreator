import pygame
from scripts.utility.scale_image import scale_image
from scripts.utility.size_element import size_element
from scripts.utility.tint_image import tint_image


class ImageStore:
    def __init__(self):
        icon_list = [("trophy", "🏆"), ("trophy2", "🏺"), ("town_hall", "🏛"), ("builder_potion", "🍷"),
                     ("capital_gold", "🪞"), ("donation", "👨"), ("preview", "👁"), ("profile", "👤"),
                     ("raid_log", "📗"), ("random", "🎲"), ("research_potion", "🔎"), ("share", "👉"), ("stopwatch", "🕰"),
                     ("war_log", "📕"), ("xp", "✹"), ("sword", "🗡"), ("spell", "🍹"), ("siege_machine", "🚗"),
                     ("elixir", "💧"), ("builder_elixir", "🩸"), ("gold", "💰"), ("builder_gold", "🪙"), ("gem", "💎"),
                     ("health", "❤"),("damage", "💥"),("view","👀"),("cross","❌"),("raid_medal","🎖")]
        self.icons2 = {}  # key = name
        self.icons = {}  # key = emoji
        for name, emoji in icon_list:
            img = pygame.image.load('assets/elements/icon/' + name + '.png').convert_alpha()
            img = scale_image(img, 50)
            self.icons[emoji],self.icons2[name] = img,img

        self.background_path, self.background = None, None
        self.element_images = {}
        self.element_images_used = []

    def get_image(self, path):
        self.element_images_used.append(path)
        if path in self.element_images.keys():
            return self.element_images[path]
        else:
            print("Loaded image to image store: ", path)
            try:
                img = pygame.image.load(path).convert_alpha()
                self.element_images[path] = img
            except FileNotFoundError:
                img = pygame.image.load('assets/editor_gui/error.png').convert_alpha()
            return img

    def get_sized_image(self, name, path, size, edge=(100, 100, 100, 100)):
        name = name + str(size)
        self.element_images_used.append(name)
        if name in self.element_images.keys():
            return self.element_images[name].copy()
        else:
            try:
                img = size_element(path, size, edge)
            except FileNotFoundError:
                img = pygame.image.load('assets/editor_gui/error.png').convert_alpha()
            self.element_images[name] = img
            print("loaded image to image store: " + name)
            return img

    def get_background(self, path):
        self.element_images_used = []

        if self.background_path != path:
            self.background_path = path
            self.background = pygame.image.load(path).convert_alpha()
        return self.background

    def get_tinted_image(self, element_type, col):
        name = element_type + str(col)
        if name in self.element_images.keys():
            self.element_images_used.append(name)
            return self.element_images[name]
        else:
            if element_type == "button":
                img = pygame.image.load('assets/elements/button/green.png').convert_alpha()
                img = tint_image(img, col, original_col=(87, 78, 80))
                self.element_images[name] = img
                self.element_images_used.append(name)
                return img
            elif element_type == "stat bars":
                print('loading', col)
                img = pygame.image.load('assets/elements/stat bars/bar2.png').convert_alpha()
                img = tint_image(img, col, original_col=(87, 74, 85))  # (144,216,56)
                self.element_images[name] = img
                self.element_images_used.append(name)
                return img

    def clear_unused_images(self):
        num_removed = 0
        dict_copy = self.element_images.copy()
        for key in dict_copy.keys():
            if str(key) not in self.element_images_used:
                del self.element_images[key]
                num_removed += 1

        if num_removed > 0:
            print("Removed " + str(num_removed) + " unused images from ImageStore")
