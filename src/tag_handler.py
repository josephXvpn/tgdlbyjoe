from pyrogram import Client, enums
import re
import tag_functions
from base_functions import find_match


def is_chat_group(message):
    if message.chat.type is enums.ChatType.GROUP or message.chat.type is enums.ChatType.SUPERGROUP:
        return True
    return False


async def add_category(client: Client, message):
    if not is_chat_group(message):
        await client.send_message(chat_id=message.chat.id, text="only can be used in groups",
                                  reply_to_message_id=message.id)
        return
    text = message.text
    category_name, usernames = process_add_text(text)
    if category_name is None or usernames is None:
        await client.send_message(chat_id=message.chat.id, text="wrong format", reply_to_message_id=message.id)
    success, user_categories = tag_functions.add_category(message.chat.id, message.from_user.id, category_name,
                                                          usernames)
    if success:
        response = f"added successfully\n```json\n{user_categories}\n```"
        await client.send_message(chat_id=message.chat.id, text=response, reply_to_message_id=message.id,
                                  parse_mode=enums.ParseMode.MARKDOWN)
    else:
        await client.send_message(chat_id=message.chat.id, text="category already exists use a different name",
                                  reply_to_message_id=message.id)


async def update_category(client: Client, message):
    if not is_chat_group(message):
        await client.send_message(chat_id=message.chat.id, text="only can be used in groups",
                                  reply_to_message_id=message.id)
        return
    text = message.text
    category_name, usernames = process_update_text(text)
    if category_name is None or usernames is None:
        await client.send_message(chat_id=message.chat.id, text="wrong format", reply_to_message_id=message.id)
    success, user_category = tag_functions.update_category(message.chat.id, message.from_user.id, category_name,
                                                           usernames)
    if success:
        response = f"updated successfully\n```json\n{user_category}\n```"
        await client.send_message(chat_id=message.chat.id, text=response, reply_to_message_id=message.id,
                                  parse_mode=enums.ParseMode.MARKDOWN)
    else:
        await client.send_message(chat_id=message.chat.id, text="category doesn't exists",
                                  reply_to_message_id=message.id)


async def get_category(client: Client, message):
    if not is_chat_group(message):
        await client.send_message(chat_id=message.chat.id, text="only can be used in groups",
                                  reply_to_message_id=message.id)
        return
    text = message.text
    _, key = find_match(text, "$category ", return_key=True)
    category_name = text[len(key):]
    category = tag_functions.get_category(message.chat.id, message.from_user.id, category_name)
    if category is None:
        await client.send_message(chat_id=message.chat.id,
                                  text=f"there is no category with name: {category_name} for you",
                                  reply_to_message_id=message.id)
    else:
        response = f"Category: {category_name}\n```json\n{category}\n```"
        await client.send_message(chat_id=message.chat.id, text=response, reply_to_message_id=message.id,
                                  parse_mode=enums.ParseMode.MARKDOWN)


async def tag_category(client: Client, message):
    username = message.from_user.username
    text = message.text
    _, key = find_match(text, "?tag ", return_key=True)
    category_name = text[len(key):]
    text_to_send = f"Hey, @{username} mentioned you\n"
    category = tag_functions.get_category(message.chat.id, message.from_user.id, category_name)
    if category is not None:
        for username in category:
            text_to_send += f"\n{username}"
        if message.reply_to_message_id:
            await client.send_message(chat_id=message.chat.id, text=text_to_send,
                                      reply_to_message_id=message.reply_to_message_id)
        else:
            await client.send_message(message.chat.id, text_to_send, reply_to_message_id=message.id)
    else:
        await client.send_message(chat_id=message.chat.id, text="can't find the category", reply_to_message_id=message.id)


def process_add_text(text):
    pattern = r'\+?\?category (\w+)\s*([\s\S]*)'
    return process_regex(text, pattern)


def process_update_text(text):
    pattern = r'\*?\?category (\w+)\s*([\s\S]*)'
    return process_regex(text, pattern)


def process_regex(text, pattern):
    match = re.match(pattern, text)
    if match:
        name = match.group(1)
        usernames = match.group(2).split()
        return name, usernames
    return None, None
