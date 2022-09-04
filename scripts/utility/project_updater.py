from scripts import common as c
from scripts.utility.file_manager import load_json, save_json


def update_project(name):
    data = load_json(name + '/data.json')
    if data["version"] in c.settings["supported_versions"]:
        if data["version"] != c.VERSION:
            print("Updating "+name+"...")
            if data["version"] == "0.1":
                update_01_to_02(name, data)
            if data["version"] == "0.2":
                update_02_to_03(name, data)
    else:
        print("ERROR: Attempted to convert project, but version number is unsupported")
        from scripts.menus.menus.project_load_error import ProjectLoadError
        c.menu = ProjectLoadError(ver=c.data["version"],supported="supported_versions")

def update_02_to_03(name,data):
    data["version"] = "0.3"
    for element in data["el"]:
        # Add 'icon size' and 'line spacing' parameters to text block
        if element[2] == "text block":
            if len(element) < 9:
                element.append(100)
                element.append(100)
        # Add 'opacity' parameter to box
        if element[2] == "box":
            if len(element) < 6:
                element.append(100)

    save_json(name + '/data.json', data)
    print("Updated to v0.3")

def update_01_to_02(name,data):
    data["version"] = "0.2"

    for element in data["el"]:
        # Add 'font' parameter to text block
        if element[2] == "text block":
            if len(element) < 8:
                element.append(small)
        # Rename 'cyan' button to 'light blue'
        elif element[2] == "button":
            if element[3] == "cyan":
                element[3] = "light blue"
        # Add 'box title' parameter to grid
        elif element[2] == "grid":
            for line in element[3]:
                for box in line:
                    if len(box) == 2:
                        box.append("")
            print(element[3])

    # Add update_speed.json
    from shutil import copyfile
    copyfile('templates/blank/update_speed.json',name + '/update_speed.json')

    save_json(name + '/data.json', data)
    print("Updated to v0.2")
