from pygame import Surface, transform, SRCALPHA


def scale_image(surf, size) -> Surface:
    width, height = size, size
    new_surf = Surface((width, height), SRCALPHA)
    if surf.get_height() > surf.get_width():
        width = surf.get_width() // (surf.get_height() / size)
    else:
        height = surf.get_height() // (surf.get_width() / size)

    # Need to add an extra blank pixel on each side, otherwise smoothscale produces hard edges
    padded_surf = Surface((surf.get_width()+2,surf.get_height()+2),SRCALPHA)
    padded_surf.blit(surf,(1,1))

    img = transform.smoothscale(padded_surf, (width, height))
    new_surf.blit(img, (new_surf.get_width() // 2 - img.get_width() // 2,
                        new_surf.get_height() // 2 - img.get_height() // 2))
    return new_surf
