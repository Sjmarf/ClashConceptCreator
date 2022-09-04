import json
import re
import ast


def special_indent_save_json(path, data):
    import io
    with io.open(path, 'w', encoding='utf-8') as f:
        s = json.dumps(data)
        s = re.sub(r'(],)', r'\1\n', s)
        s = re.sub(r'(",)', r'\1\n', s)
        f.write(s)


def save_json(path, data):
    import json
    with open(path, "w") as outfile:
        json.dump(data, outfile)


def load_json(path):
    import json
    data = json.load(open(path))
    return data

def load_json_base_design(path):
    # Replaces lists with tuples (tuples don't work in dicts)
    data = load_json(path)
    converted_dict = {}
    for k, v in data["el"].items():
        converted_dict[ast.literal_eval(k)] = v
    data["el"] = converted_dict
    return data

def save_json_base_design(path, data):
    # Replaces tuples with lists (JSON can't save tuples)
    converted_dict = {}
    for k, v in data["el"].items():
        converted_dict[str(k)] = v
    data["el"] = converted_dict
    save_json(path, data)

def get_file_list(location):
    import os
    path = os.getcwd() + "/" + location
    list1 = os.listdir(path)
    if ".DS_Store" in list1:
        list1.remove(".DS_Store")
    del os
    return list1
