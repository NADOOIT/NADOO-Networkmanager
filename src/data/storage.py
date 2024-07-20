import json
import os
from src.config import DATA_FILE_PATH


def read_data():
    if os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    else:
        return {"users": [], "folienvorlagen": []}


def write_data(data):
    with open(DATA_FILE_PATH, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def delete_element(data, element_id):
    pass


def get_users():
    return [user for user in read_data()['users']]
