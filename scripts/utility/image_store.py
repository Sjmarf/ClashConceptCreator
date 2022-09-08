import pygame
from scripts import common as c
from scripts.utility.scale_image import scale_image
from scripts.utility.size_element import size_element
from scripts.utility.tint_image import tint_image, get_monochrome_image
from copy import deepcopy


class ImageStore:
    def __init__(self):

        self.background_path, self.background = None, None
        self.element_images = {}
        self.element_images_used = []

    def get_image(self, path):
        self.element_images_used.append(path)
        c.images_used.append(path.split("/")[-1])
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

    def get_scaled_image(self, path, scale, show_error_image=True):
        name = path+" "+str(scale)
        self.element_images_used.append(name)
        c.images_used.append(path.split("/")[-1])
        if name in self.element_images.keys():
            return self.element_images[name]
        else:
            try:
                img = pygame.image.load(path).convert_alpha()
                img = scale_image(img,scale)
                self.element_images[name] = img
                print("Loaded scaled image to image store: ", path)
            except FileNotFoundError:
                if show_error_image:
                    img = pygame.image.load('assets/editor_gui/error.png').convert_alpha()
                    img = scale_image(img, scale)
                else:
                    return None
            return img

    def get_sized_image(self, name, path, size, edge=(100, 100, 100, 100)):
        name = name + str(size)
        self.element_images_used.append(name)
        c.images_used.append(path.split("/")[-1])
        if name in self.element_images.keys():
            return self.element_images[name].copy()
        else:
            try:
                img = size_element(path, size, edge)
                self.element_images[name] = img
            except FileNotFoundError:
                img = pygame.Surface(size, pygame.SRCALPHA)
                error_img = pygame.image.load('assets/editor_gui/error.png').convert_alpha()
                error_img = scale_image(error_img,size[1])
                img.blit(error_img,(img.get_width()//2-error_img.get_width()//2,0))
            print("loaded image to image store: " + name)
            return img.copy()

    def get_monochrome_image(self,path):
        self.element_images_used.append(path.split("/")[-1])
        name = path + " (monochrome)"
        self.element_images_used.append(name)
        if name in self.element_images.keys():
            return self.element_images[name].copy()
        else:
            try:
                img = pygame.image.load(path).convert_alpha()
                img = get_monochrome_image(img)
                self.element_images[name] = img
            except FileNotFoundError:
                img = pygame.image.load('assets/editor_gui/error.png').convert_alpha()
            return img.copy()

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
            if element_type == "tinted_button":
                img = pygame.image.load('assets/elements/button/green.png').convert_alpha()
                img = tint_image(img, col, original_col=(87, 78, 80))
                self.element_images[name] = img
                self.element_images_used.append(name)
                return img
            elif element_type == "stat_bars":
                print('loading', col)
                img = pygame.image.load('assets/elements/stat bars/stat/bar2.png').convert_alpha()
                img = tint_image(img, col, original_col=(87, 74, 85))  # (144,216,56)
                self.element_images[name] = img
                self.element_images_used.append(name)
                return img
        print("NONE FOUND")

    def clear_unused_images(self):
        num_removed = 0
        dict_copy = self.element_images.copy()
        for key in dict_copy.keys():
            if str(key) not in self.element_images_used:
                del self.element_images[key]
                num_removed += 1

        if num_removed > 0:
            print("Removed " + str(num_removed) + " unused images from ImageStore")
