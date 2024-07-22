from pyrogram import Client, enums
import data
import threading
import requests
import json

base_url = "http://localhost:14288/"
tag_maps = {}


def find_match(text, keys, same_as_key=False, return_key=False):
    if isinstance(keys, str):
        keys = [keys]

    for key in keys:
        chosen_key = None
        found = False
        if same_as_key:
            if text == key:
                chosen_key = key
                found = True
        else:
            if text == key or text.startswith(key):
                chosen_key = key
                found = True

        if found:
            if return_key:
                return True, chosen_key
            else:
                return True
    if return_key:
        return False, None
    else:
        return False


async def tag_all(client: Client, message):
    username = message.from_user.username
    text_to_send = f"Hey everybody, @{username} mentioned all of you\n"
    async for member in client.get_chat_members(chat_id=message.chat.id):
        un = member.user.username
        if un:
            if un != username:
                text_to_send += "@" + un + "\n"
    if message.reply_to_message_id:
        await client.send_message(chat_id=message.chat.id, text=text_to_send,
                                  reply_to_message_id=message.reply_to_message_id)
    else:
        await client.send_message(message.chat.id, text_to_send)


async def send_guide(chat_id, msg_id, client: Client):
    await client.send_message(chat_id, data.get_guide(), reply_to_message_id=msg_id, parse_mode=enums.ParseMode.HTML)


def generate_json_object(chat_id, msg_id, url, stat_msg_id, quality_code=0, timestamp=None,
                         chapter_name=None, large_file=False):
    return {"url": url, "chat_id": chat_id, "msg_id": msg_id, "timestamp": timestamp,
            "quality_code": quality_code,
            "chapter_name": chapter_name,
            "large_file": large_file,
            "stat_msg_id": stat_msg_id}


def send_post_request(url, json_data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(base_url + url, json=json_data, headers=headers)
    return response
