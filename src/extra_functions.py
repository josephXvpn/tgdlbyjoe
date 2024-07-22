from pyrogram import Client

spotify_queue = []


async def handle_spotify_download(client: Client, message):
    spotify_queue.append({"msg_id": message.id, "chat_id": message.chat.id})
    await client.send_message(chat_id="DeezerMusicBot", text=message.text)


async def handle_deezer_bot_response(client: Client, message):
    if spotify_queue:
        oldest_req = spotify_queue.pop(0)
        if message.audio:
            await client.copy_message(oldest_req["chat_id"], "DeezerMusicBot", message.id,
                                      reply_to_message_id=oldest_req["msg_id"], caption="")
        else:
            await client.send_message(chat_id=oldest_req["chat_id"], text="can't find the music",
                                      reply_to_message_id=oldest_req["msg_id"])
