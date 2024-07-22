import os

from base_functions import find_match
from pyrogram import Client, filters, compose
import base_video_functions
import base_functions
import extra_functions
import asyncio
import yt_dlp
import video_functions
import tag_handler

uk = {
    "api_id": 16977468,
    "api_hash": 'c439e1f382f236fe14bca265f5cba50c',
    "phone_number": '+44 7852 751004'
}
ru = {
    "api_id": 24616732,
    "api_hash": '4f8b1b1f89501184074eb5a2f6d86592',
    "phone_number": '+79211561855'
}

session_folder = '/etc/tgdl/sessions/'
os.makedirs(session_folder, exist_ok=True)

app_ru = Client(os.path.join(session_folder, "ru"), api_id=ru["api_id"], api_hash=ru["api_hash"], phone_number=ru["phone_number"])
app_uk = Client(os.path.join(session_folder, "uk"), api_id=uk["api_id"], api_hash=uk["api_hash"], phone_number=uk["phone_number"])


video_id = 1

baseUrl = "http://localhost:14288/"
ydl = yt_dlp.YoutubeDL({})

geminiReqID = 1


@app_uk.on_message(filters.private)
async def handle_messages(client, message):
    await handle_message(client, message)


@app_ru.on_message(
    filters.private | filters.bot | filters.chat(-1001779355612) | filters.chat(-4171857637) | filters.chat(
        -1002107202080) | filters.chat(-4009353443))
async def handle_messages(client, message):
    await handle_message(client, message)


async def handle_message(client, message):
    message_text = message.text
    if message_text is not None:
        if find_match(message_text, ["?guide", "?help"], True):
            await base_functions.send_guide(message.chat.id, message.id, client)
        elif find_match(message_text, "?tag all", True):
            await base_functions.tag_all(client, message)
        elif find_match(message_text, "+?category "):
            await tag_handler.add_category(client, message)
        elif find_match(message_text, "*?category "):
            await tag_handler.update_category(client, message)
        elif find_match(message_text, "$category "):
            await tag_handler.get_category(client, message)
        elif find_match(message_text, "?tag "):
            await tag_handler.tag_category(client, message)
        elif find_match(message_text, "https://www.instagram.com"):
            await video_functions.download_video_ig(message.chat.id, message.id, message_text, client)
        elif find_match(message_text, ["????", "/porn "]):
            await base_video_functions.download_large_video(client, message)
        elif find_match(message_text, ["/yv ", "/v ", "???"]):
            await base_video_functions.download_yt_hq(client, message)
        elif find_match(message_text, "https://open.spotify"):
            await extra_functions.handle_spotify_download(client, message)
        elif find_match(message_text, ["??", "/cyt "]):
            await base_video_functions.handle_custom_ytdl_request(client=client, message=message)
        elif find_match(message_text, ["?1080+", "?720", "?360"]):
            await base_video_functions.handle_custom_ytdl_response(client, message)
        elif find_match(message_text, ["?", "/yt "]):
            await asyncio.create_task(base_video_functions.download_yt_mp3(client, message))
        elif message.from_user.username == "DeezerMusicBot":
            await extra_functions.handle_deezer_bot_response(client, message)
    else:
        user_name = message.from_user.username
        if user_name == "DeezerMusicBot":
            await extra_functions.handle_deezer_bot_response(client, message)


def main():
    apps = [
        app_uk,
        app_ru
    ]
    asyncio.run(compose(apps))


main()
