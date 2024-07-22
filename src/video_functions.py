import yt_dlp
from pyrogram import Client
import base_functions
from moviepy.editor import VideoFileClip
import igdl
import wget
import thumbex
import upload_functions


ydl = yt_dlp.YoutubeDL({})


def get_available_qualities(url):
    info_dict = ydl.extract_info(url=url, download=False)
    format_18_available = any(format['format_id'] == '18' for format in info_dict['formats'])
    format_22_available = any(format['format_id'] == '22' for format in info_dict['formats'])
    return [format_18_available, format_22_available]


def get_video_resolution(video_path):
    video = VideoFileClip(video_path)
    width, height = video.size
    return width, height


def get_video_duration(file_path):
    clip = VideoFileClip(file_path)
    duration = clip.duration
    clip.close()
    return duration


async def download_video_hq(chat_id, msg_id, url, client: Client):
    stat_msg = await client.send_message(chat_id, "✅Downloading...⏳🎦")
    req_body = base_functions.generate_json_object(chat_id=chat_id,
                                                   msg_id=msg_id,
                                                   url=url,
                                                   stat_msg_id=stat_msg.id)
    response = base_functions.send_post_request("dl_vid", req_body)
    return response


async def download_large_videos(chat_id, msg_id, url, client: Client):
    stat_msg = await client.send_message(chat_id, "✅Downloading...⏳🔞")
    req_body = base_functions.generate_json_object(chat_id=chat_id,
                                                   msg_id=msg_id,
                                                   url=url,
                                                   large_file=True,
                                                   stat_msg_id=stat_msg.id)
    response = base_functions.send_post_request("dl_vid", req_body)
    return response


async def download_video_ig(chat_id, msg_id, url, client: Client):
    stat_msg = await client.send_message(chat_id=chat_id, text="✅Downloading...⏳🎦")
    ab_url, uri_name = igdl.get_absolute_video_url(url)
    if ab_url is not None and uri_name is not None:
        video_path = f"./{uri_name}.mp4"
        thumb_path = f"./{uri_name}.jpg"
        wget.download(url=ab_url, out=video_path)
        thumbex.extract_thumbnail(video_path=video_path, frame_number=88, thumbnail_path=thumb_path)
        caption = igdl.get_title_and_author_name(url)
        await upload_functions.upload_ig_video(client, chat_id, stat_msg.id, msg_id, video_path, thumb_path, caption)
    else:
        await client.edit_message_text(stat_msg.chat.id, stat_msg.id,
                                       "❌wrong link (stories and photos are not supported)❌")


async def download_audio(chat_id, msg_id, url, client: Client):
    stat_msg = await client.send_message(chat_id, "✅Downloading...⏳🎶")
    req_body = base_functions.generate_json_object(chat_id=chat_id, msg_id=msg_id, url=url,
                                                   stat_msg_id=stat_msg.id)
    response = base_functions.send_post_request("dl_mp3", req_body)
    return response.text
