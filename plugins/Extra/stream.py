from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from info import URL, LOG_CHANNEL
from urllib.parse import quote_plus
from LucyBot.util.file_properties import get_name, get_hash, get_media_file_size
from LucyBot.util.human_readable import humanbytes
import humanize
import random

@Client.on_message(filters.private & filters.command("stream"))
async def stream_start(client, message):
    msg = await client.ask(message.chat.id, "**Now send me your file/video to get stream and download link**")
    if not msg.media:
        return await message.reply("**Please send me supported media.**")
    if msg.media in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
        file = getattr(msg, msg.media.value)
        filename = file.file_name
        filesize = humanize.naturalsize(file.file_size) 
        fileid = file.file_id
        user_id = message.from_user.id
        username =  message.from_user.mention 

        log_msg = await client.send_cached_media(
            chat_id=LOG_CHANNEL,
            file_id=fileid,
        )
        fileName = {quote_plus(get_name(log_msg))}
        stream = f"{URL}watch/{str(log_msg.id)}?hash={get_hash(log_msg)}"
        download = f"{URL}{str(log_msg.id)}?hash={get_hash(log_msg)}"
 
        await log_msg.reply_text(
            text=f"# link generation \n restricted by admin",
            quote=True,
            disable_web_page_preview=True
        )
        rm=InlineKeyboardMarkup(
            [
                [
             
                    InlineKeyboardButton(' contact owner', url='https://t.me/infinitybm')
                ]
            ] 
        )
        msg_text = """<i><u>I am not providing this feature because my owner said noo!</u></i>"""

        await message.reply_text(text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(msg)), download, stream), quote=True, disable_web_page_preview=True, reply_markup=rm)
