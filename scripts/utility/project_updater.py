from scripts.utility.file_manager import loadJson, saveJson


def update_project(name):
    update_01_to_02(name)


def update_01_to_02(name):
    data = loadJson('projects/' + name + '/data.json')
    data["version"] = "0.2"

    for element in data["el"]:
        # Add 'font' parameter to text block
        if element[2] == "text block":
            if len(element) < 7:
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
    copyfile('templates/blank/update_speed.json','projects/' + name + '/update_speed.json')

    saveJson('projects/' + name + '/data.json',data)
    print("CONVERTED")
