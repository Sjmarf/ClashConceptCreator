from pygame import Surface, transform, SRCALPHA


def scale_image(surf, size) -> Surface:
    if type(size) == int or type(size) == float:
        size = (size, size)

    width, height = size
    new_surf = Surface((width, height), SRCALPHA)
    height = surf.get_height() // (surf.get_width() / size[0])
    if height > size[1]:
        width = surf.get_width() // (surf.get_height() / size[0])
        height = size[1]
    img = transform.smoothscale(surf, (width, height))
    new_surf.blit(img, (size[0] // 2 - width // 2, size[1] // 2 - height // 2))
    return new_surf
