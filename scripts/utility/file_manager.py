import json
import re


def special_indent_save_json(path, data):
    import io
    with io.open(path, 'w', encoding='utf-8') as f:
        s = json.dumps(data)
        s = re.sub(r'(],)', r'\1\n', s)
        s = re.sub(r'(",)', r'\1\n', s)
        f.write(s)


def saveJson(path, data, indent=None):
    import json
    with open(path, "w") as outfile:
        json.dump(data, outfile, indent=indent)


def loadJson(path):
    import json
    data = json.load(open(path))
    return data


def getFileList(location):
    import os
    path = os.getcwd() + "/" + location
    list1 = os.listdir(path)
    if ".DS_Store" in list1:
        list1.remove(".DS_Store")
    del os
    return list1
