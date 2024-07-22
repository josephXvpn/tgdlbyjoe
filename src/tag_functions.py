import json
import os


json_file_path = "tag_data.json"


def read_json_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            json_data = json.load(file)
            return json_data
    else:
        return {}


tag_map = read_json_data(json_file_path)


def get_category(group_id, user_id, category_name):
    if group_id in tag_map:
        if user_id in tag_map.get(group_id):
            if category_name in tag_map.get(group_id).get(user_id):
                return tag_map.get(group_id).get(user_id).get(category_name)
    return None


def add_category(group_id, user_id, category_name, category_usernames):
    if group_id not in tag_map:
        tag_map[group_id] = {}
    group_map = tag_map.get(group_id)
    if user_id not in group_map:
        group_map[user_id] = {}
    if category_name not in group_map.get(user_id):
        group_map.get(user_id)[category_name] = category_usernames
        tag_map[group_id] = group_map
        write_json_data(tag_map)
        return True, group_map.get(user_id)
    else:
        return False, None


def update_category(group_id, user_id, category_name, category_usernames):
    category = get_category(group_id, user_id, category_name)
    if category is None:
        return False, None
    tag_map.get(group_id).get(user_id)[category_name] = category_usernames
    write_json_data(tag_map)
    return True, get_category(group_id, user_id, category_name)


def delete_category(group_id, user_id, category_name):
    category = get_category(group_id, user_id, category_name)
    if category is None:
        return False, None
    deleted_category = tag_map.get(group_id).get(user_id).pop(category_name)
    write_json_data(tag_map)
    return True, deleted_category


def write_json_data(json_data):
    global json_file_path
    with open(json_file_path, "w") as file:
        json.dump(json_data, file)
