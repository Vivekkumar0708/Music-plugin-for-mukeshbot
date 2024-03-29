from pyrogram import Client
from pyrogram.types import Message
from pyrogram import filters
from pyrogram.types import(InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo, Message)
from config import LOGGER_ID as LOG_GROUP_ID
from VIPMUSIC import app  




@app.on_message(filters.new_chat_members, group=2)
async def join_watcher(_, message):    
    chat = message.chat
    for members in message.new_chat_members:
        if members.id == app.id:
            count = await app.get_chat_members_count(chat.id)
            username = message.chat.username if message.chat.username else "ᴘʀɪᴠᴀᴛᴇ ɢʀᴏᴜᴘ"
            msg = (
                f"**ᴍᴜsɪᴄ ʙᴏᴛ ᴀᴅᴅᴇᴅ ɪɴ ᴀ ɴᴇᴡ ɢʀᴏᴜᴘ #ɴᴇᴡ_ɢʀᴏᴜᴘ**\n\n"
                f"**ᴄʜᴀᴛ ɴᴀᴍᴇ:** {message.chat.title}\n"
                f"**ᴄʜᴀᴛ ɪᴅ:** {message.chat.id}\n"
                f"**ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :** @{username}\n"
                f"**ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀs:** {count}\n"
                f"**ᴀᴅᴅᴇᴅ ʙʏ:** {message.from_user.mention}"
            )
            await app.send_message(LOG_GROUP_ID, text=msg)



@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    if (await app.get_me()).id == message.left_chat_member.id:
        remove_by = message.from_user.mention if message.from_user else "𝐔ɴᴋɴᴏᴡɴ 𝐔sᴇʀ"
        title = message.chat.title
        username = f"@{message.chat.username}" if message.chat.username else "𝐏ʀɪᴠᴀᴛᴇ 𝐂ʜᴀᴛ"
        chat_id = message.chat.id
        left = f"""
✫ <b><u>#ʟᴇғᴛ_ɢʀᴏᴜᴘ</u></b> ✫
ᴄʜᴀᴛ ᴛɪᴛʟᴇ : {title}
ᴄʜᴀᴛ ɪᴅ : {chat_id}
ʀᴇᴍᴏᴠᴇᴅ ʙʏ : {remove_by}"""
        await app.send_message(LOG_GROUP_ID, text=left)


