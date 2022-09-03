import pygame
from scripts import common as c


class FontObject:
    def __init__(self, text, preset, size):
        self.text, self.preset, self.size = text, preset, size
        self.img = renderText(text, preset, size)

    def render(self, surface, pos, centre=False):
        if centre:
            surface.blit(self.img, (surface.get_width() // 2 - self.img.get_width() // 2, pos[1]))
        else:
            surface.blit(self.img, pos)

    def setText(self, text):
        if not text == self.text:
            self.text = text
            self.img = renderText(text, self.preset, self.size)


def renderText(text, preset, size, font_type='large', border=0, thickness=0, col=(255, 255, 255), outline_col=(0, 0, 0)) \
        -> pygame.Surface:
    # Presets :
    #    Default
    #    Small1 (used to show 'Played recently' under user's name in clan settings)
    #    Small2 (darker version of Small1)
    # font can be 'small' (font name: Back Beat) or 'large' (font name: Supercell Magic)

    if preset != "custom":
        presets = {
            "default": ('large', max(1.1, size / 25), max(3,size // 6.25), (255, 255, 255), (0, 0, 0)),
            "small1": ('small', 0, 0, (131, 129, 118), (0, 0, 0)),
            "small2": ('small', 0, 0, (107, 104, 95), (0, 0, 0))
        }
        font_type, border, thickness, col, outline_col = presets[preset]

    smoothscale_size_method = True  # Set to True to enable experimental method of sizing the text, to remove
    # undesirable effects when using very small text
    smoothscale_orig_size = size*2
    keys = pygame.key.get_pressed()
    if keys[pygame.K_p]:
        smoothscale_size_method = False

    if smoothscale_size_method:
        supercell = pygame.font.Font('assets/fonts/' + font_type + '.ttf', smoothscale_orig_size)
        test_font = pygame.font.Font('assets/fonts/' + font_type + '.ttf', size)
        scale_factor = smoothscale_orig_size/size
        offset = 10
        orig_thickness = thickness
        border,thickness = border*scale_factor,thickness*scale_factor*1.2
    else:
        supercell = pygame.font.Font('assets/fonts/' + font_type + '.ttf', size)
        offset = 10

    black = supercell.render(text, True, outline_col)
    white = supercell.render(text, True, col)

    main_surf = pygame.Surface((black.get_width() + offset * 2, black.get_height() + offset * 2 + thickness), pygame.SRCALPHA)

    if not border == 0:
        # Drop-down
        main_surf.blit(black, (offset - border, offset + thickness))
        main_surf.blit(black, (offset + border, offset + thickness))
        main_surf.blit(black, (offset - border, offset + thickness // 2))
        main_surf.blit(black, (offset + border, offset + thickness // 2))

        # Black border
        main_surf.blit(black, (offset - border, offset - border))
        main_surf.blit(black, (offset + border, offset + border))
        main_surf.blit(black, (offset - border, offset + border))
        main_surf.blit(black, (offset + border, offset - border))

    # Main text
    main_surf.blit(white, (offset, offset))

    if smoothscale_size_method:
        test_surf = test_font.render(text,True,(0,0,0))
        width,height = test_surf.get_size()
        x_offset = (offset/smoothscale_orig_size)*size*2
        y_offset = x_offset+(orig_thickness)/smoothscale_orig_size*size/1.2
        surf = pygame.transform.smoothscale(main_surf, (width+x_offset,
                                                             height+y_offset))
        main_surf = pygame.Surface((width+offset*2-x_offset,height+offset*2-y_offset+orig_thickness),pygame.SRCALPHA)
        main_surf.blit(surf,(main_surf.get_width()//2-surf.get_width()//2,
                             main_surf.get_height()//2-surf.get_height()//2))

    return main_surf
