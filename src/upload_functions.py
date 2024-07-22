import glob
import json
import os
import video_functions
from pyrogram import Client
import time

last_time = 0
last_msg_prog = ""


async def upload_audio(client: Client, audio_res):
    response_dict = json.loads(audio_res)
    success = response_dict.get('success')
    data = response_dict.get('data')

    chat_id = data.get('chat_id')
    msg_id = data.get('msg_id')

    if not success:
        res_msg = response_dict.get('resMsg')
        await client.send_message(chat_id=chat_id, text=res_msg, reply_to_message_id=msg_id)
        return

    path = data.get('path')

    if not path:
        await client.send_message(chat_id=chat_id, text="something wrong with the path", reply_to_message_id=msg_id)
        return

    thumbnail = path + "thumbnail.jpg"
    stat_msg_id = data.get('stat_msg_id')

    mp3_files = glob.glob(os.path.join(path, '*.mp3'))
    if mp3_files:
        audio_file_path = mp3_files[0]
    else:
        await client.send_message(chat_id=chat_id, text="Error: No MP3 files found", reply_to_message_id=msg_id)
        return

    kwargs = {
        'chat_id': chat_id,
        'audio': audio_file_path,
        'progress': progress
    }

    if msg_id != 0:
        kwargs['reply_to_message_id'] = msg_id

    if thumbnail is not None:
        kwargs['thumb'] = thumbnail

    await client.send_audio(**kwargs, progress_args=tuple([int(stat_msg_id), int(chat_id), client]))
    try:
        audio_directory = os.path.dirname(audio_file_path)
        for filename in os.listdir(audio_directory):
            file_path = os.path.join(audio_directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
    except Exception as e:
        print(f"Error deleting video: {e}")


async def upload_video(client: Client, video_res):
    response_dict = json.loads(video_res)
    success = response_dict.get('success')
    data = response_dict.get('data')

    chat_id = data.get('chat_id')
    msg_id = data.get('msg_id')

    if not success:
        res_msg = response_dict.get('resMsg')
        await client.send_message(chat_id=chat_id, text=res_msg, reply_to_message_id=msg_id)
        return

    path = data.get('path')
    if not path:
        await client.send_message(chat_id=chat_id, text="Something went wrong with the path", reply_to_message_id=msg_id)
        return

    thumbnail = os.path.join(path, "thumbnail.jpg")
    stat_msg_id = data.get('stat_msg_id')

    video_files = glob.glob(os.path.join(path, '*.mp4')) + glob.glob(os.path.join(path, '*.webm'))
    if video_files:
        video_file_path = video_files[0]
    else:
        await client.send_message(chat_id=chat_id, text="Error: No MP4 or WEBM files found", reply_to_message_id=msg_id)
        return

    width, height = video_functions.get_video_resolution(video_file_path)
    duration = int(video_functions.get_video_duration(video_file_path))
    kwargs = {
        'chat_id': chat_id,
        'video': video_file_path,
        'width': width,
        'height': height,
        'progress': progress,
        'duration': duration,
        'reply_to_message_id': msg_id
    }
    if thumbnail is not None and os.path.exists(thumbnail):
        kwargs['thumb'] = thumbnail
    else:
        print("Warning: 'thumbnail' is not specified or does not exist")

    await client.send_video(**kwargs, progress_args=(stat_msg_id, chat_id, client))

    try:
        video_directory = os.path.dirname(path)
        for filename in os.listdir(video_directory):
            file_path = os.path.join(video_directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
    except Exception as e:
        print(f"Error deleting video: {e}")


async def upload_ig_video(client: Client, chat_id, stat_msg_id, req_msg_id, video_path, thumb_path, caption):
    width, height = video_functions.get_video_resolution(video_path)
    duration = int(video_functions.get_video_duration(video_path))

    kwargs = {
        'chat_id': chat_id,
        'video': video_path,
        'width': width,
        'height': height,
        'caption': caption,
        'progress': progress,
        'duration': duration,
        'thumb': thumb_path,
        'reply_to_message_id': req_msg_id
    }
    await client.send_video(**kwargs, progress_args=tuple([int(stat_msg_id), int(chat_id), client]))
    os.unlink(video_path)
    os.unlink(thumb_path)


async def progress(current, total, msg_id, chat_id, client: Client):
    global last_time
    global last_msg_prog
    current_time = time.time() * 1000  # Convert current time to milliseconds
    percent = current * 100 / total
    if percent >= 100:
        msg = "✅ 100% Request Completed ✅"
        if last_msg_prog != msg:
            last_msg_prog = msg
            await client.edit_message_text(message_id=msg_id, chat_id=chat_id, text=msg)

    if percent > 95.0 or current_time - last_time < 2888:
        return
    else:
        msg = f"⏳ Uploading... {percent:.1f}%"
        if last_msg_prog != msg:
            last_msg_prog = msg
            await client.edit_message_text(message_id=msg_id, chat_id=chat_id, text=msg)

    last_time = time.time() * 1000
