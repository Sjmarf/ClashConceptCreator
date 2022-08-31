from scripts import common as c
from scripts.utility.scale_image import scale_image
import pygame.image


def renderImage(element):
    data = c.data["el"][element]
    if data[3] is not None:
        img = c.image_store.get_image('projects/' + c.project_name + '/images/' + data[3] + '.png')
        c.images_used.append(data[3] + ".png")
        size = min(data[1]) * (data[4] / 100)
        img = scale_image(img, size)
        # surf.blit(img,(data[0][0]+data[1][0]//2-size//2,data[0][1]+data[1][1]//2-size//2))

        # Calculate if this image should be used for project icon
        if data[1][0] * data[1][1] > c.icon_image[1]:
            c.icon_image = (data[3] + ".png", data[1][0] * data[1][1])

        # This is needed for image sizing
        surf = pygame.Surface(data[1], pygame.SRCALPHA)
        surf.blit(img, (data[1][0] // 2 - size // 2, data[1][1] // 2 - size // 2))

        return surf
