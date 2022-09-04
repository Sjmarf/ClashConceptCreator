from scripts.utility.file_manager import get_file_list,save_json,load_json


def duplicate(data,name):
    from shutil import copytree,ignore_patterns
    num = 2
    new_name = name + str(num)
    while new_name in get_file_list('projects/'):
        new_name = name + str(num)
        num += 1
    copytree('projects/' + name, 'projects/' + new_name, ignore=ignore_patterns(".DS_Store"))

    if "/" not in name:
        data.append(new_name)
    else:
        folder, name = name.split("/")
        print(folder, name)
        for item in data:
            if type(item) == list:
                if item[0] == folder:
                    item.append(new_name.split("/")[1])
    save_json('projects/projects.json', data)

def delete(data,name):
    import shutil

    if "/" in name:
        folder_name, name = name.split("/")
        folder_index = None
        for num, i in enumerate(data):
            if type(i) == list:
                if i[0] == folder_name:
                    folder_index = num
                    break
        if folder_index is None:
            print("Deletion index error: file folder not found")
        else:
            index = data[folder_index].index(name)
            del data[folder_index][index]
        # Remove the project file
        shutil.rmtree('projects/' + folder_name + "/" + name)

    elif "FOLDER" in name:
        index = None
        name = name.replace("FOLDER ", "")
        for num, i in enumerate(data):
            if type(i) == list:
                if i[0] == name:
                    index = num
        del data[index]
        try:
            shutil.rmtree('projects/' + name)
        except FileNotFoundError:
            print("Couldn't find a directory to delete, skipping deletion")
    else:
        index = data.index(name)

        # This if-statement is just a failsafe incase something goes wrong
        if index is not None:
            del data[index]
            # Remove the project file
            shutil.rmtree('projects/' + name)
        else:
            print("Deletion index error: File not found")
    save_json('projects/projects.json', data)
