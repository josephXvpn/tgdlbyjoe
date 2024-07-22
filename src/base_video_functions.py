from pyrogram import Client, enums
import video_functions
import base_functions
import upload_functions

custom_yt_map = {}


async def download_yt_mp3(client: Client, message):
    message_text = message.text
    _, key = base_functions.find_match(message_text, ["?", "/yt "], return_key=True)
    url = message_text[len(key):]
    resp = await video_functions.download_audio(message.chat.id, message.id, url, client)
    await upload_functions.upload_audio(client, resp)


async def download_yt_hq(client: Client, message):
    message_text = message.text
    _, key = base_functions.find_match(message_text, ["/yv ", "/v ", "???"], return_key=True)
    url = message_text[len(key):]
    resp = await video_functions.download_video_hq(message.chat.id, message.id, url, client)
    await upload_functions.upload_video(client, resp)


async def download_large_video(client: Client, message):
    message_text = message.text
    _, key = base_functions.find_match(message_text, ["????", "/porn"], return_key=True)
    url = message_text[len(key):]
    resp = await video_functions.download_large_videos(message.chat.id, message.id, url, client)
    await upload_functions.upload_video(client, resp)


async def handle_custom_ytdl_request(client: Client, message):
    message_text = message.text
    _, key = base_functions.find_match(message_text, ["/cyt ", "??"], return_key=True)
    url = message_text[len(key):]
    available_qualities = video_functions.get_available_qualities(url)
    custom_yt_map[message.from_user.id] = {"url": url, "avq": available_qualities, "req_msg_id": message.id}
    response = "Available Qualities:"
    response += f"\n     <b>HQ</b>: <code>?1080+</code>"
    if available_qualities[1]:
        response += f"\n     <b>720</b>: <code>?720</code>"
    if available_qualities[0]:
        response += f"\n     <b>360</b>: <code>?360</code>"
    qlist_msg_id = await client.send_message(chat_id=message.chat.id, text=response, parse_mode=enums.ParseMode.HTML)
    custom_yt_map[message.from_user.id]["qlist_msg_id"] = qlist_msg_id


async def handle_custom_ytdl_response(client: Client, message):
    user_id = message.from_user.id
    if user_id in custom_yt_map:
        msg_text = message.text
        qcode = get_quality_code(msg_text)
        if is_quality_available(qcode, custom_yt_map[user_id].get('avq')):
            req_msg_id = custom_yt_map[user_id].get('req_msg_id')
            url = custom_yt_map[user_id].get('url')
            stat_msg = custom_yt_map[user_id].get('qlist_msg_id')
            req_body = base_functions.generate_json_object(chat_id=message.chat.id,
                                                           msg_id=req_msg_id,
                                                           url=url,
                                                           stat_msg_id=stat_msg.id,
                                                           quality_code=qcode)
            await client.edit_message_text(chat_id=message.chat.id, message_id=stat_msg.id,
                                           text=f"{stat_msg.text}\n✅Accepted",
                                           parse_mode=enums.ParseMode.HTML)
            dl_resp = base_functions.send_post_request("dl_vid", json_data=req_body)
            await upload_functions.upload_video(client=client, video_res=dl_resp)
            custom_yt_map[user_id] = None
        else:
            await client.send_message(message.chat.id, text="Quality not available", reply_to_message_id=message.id)


def get_quality_code(text):
    if text == "?1080+":
        return 0
    elif text == "?720":
        return 22
    elif text == "?360":
        return 18
    else:
        return -1


def is_quality_available(qcode, available_qualities):
    if qcode == 18:
        if available_qualities[0]:
            return True
    if qcode == 22:
        if available_qualities[1]:
            return True
    if qcode == 88:
        return True
    return False
