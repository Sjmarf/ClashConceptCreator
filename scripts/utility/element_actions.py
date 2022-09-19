from scripts import common as c
from copy import deepcopy


def layer_up():
    if c.selected[0] == len(c.data["el"]) - 1:
        print("TOP")
    else:
        data = c.data["el"].pop(c.selected[0])
        c.selected[0] += 1
        c.data["el"].insert(c.selected[0], data)
        c.menu.canvas.draw()
        c.menu.side_bar.changeMenu()


def layer_down():
    if c.selected[0] == 1:
        print("BOTTOM")
    else:
        data = c.data["el"].pop(c.selected[0])
        c.selected[0] -= 1
        c.data["el"].insert(c.selected[0], data)
        c.menu.canvas.draw()
        c.menu.side_bar.changeMenu()


def delete():
    del c.data["el"][c.selected[0]]
    c.menu.canvas.draw()
    c.selected = None
    c.menu.side_bar.changeMenu()


def duplicate():
    new = deepcopy(c.data["el"][c.selected[0]])
    c.data["el"].append(new)
    c.selected[0] = len(c.data["el"]) - 1
    c.menu.side_bar.changeMenu()
    c.menu.bottom_bar.feedback_text = ["Duplicated",20]
