from typing import Dict, List, Union
from config import MONGO_DB_URI
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram import filters
from pyrogram.types import Message
from VIPMUSIC import app
from VIPMUSIC.utils.vip_ban import admin_filter

mongo = MongoCli(MONGO_DB_URI).Rankings

impdb = mongo.pretender

async def usr_data(chat_id: int, user_id: int) -> bool:
    user = await impdb.find_one({"chat_id": chat_id, "user_id": user_id})
    return bool(user)

async def get_userdata(chat_id: int, user_id: int) -> Union[Dict[str, str], None]:
    user = await impdb.find_one({"chat_id": chat_id, "user_id": user_id})
    return user

async def add_userdata(chat_id: int, user_id: int, username: str, first_name: str, last_name: str):
    await impdb.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {
            "$set": {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            }
        },
        upsert=True,
    )

async def check_pretender(chat_id: int) -> bool:
    chat = await impdb.find_one({"chat_id_toggle": chat_id})
    return bool(chat)

async def impo_on(chat_id: int) -> None:
    await impdb.insert_one({"chat_id_toggle": chat_id})

async def impo_off(chat_id: int) -> None:
    await impdb.delete_one({"chat_id_toggle": chat_id})

@app.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=69)
async def chk_usr(_, message: Message):
    chat_id = message.chat.id
    if message.sender_chat or not await check_pretender(chat_id):
        return
    if not await usr_data(chat_id, message.from_user.id):
        return await add_userdata(
            chat_id,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    user_data = await get_userdata(chat_id, message.from_user.id)
    if not user_data:
        return  # User data not found, handle accordingly
    usernamebefore = user_data.get("username", "")
    first_name = user_data.get("first_name", "")
    lastname_before = user_data.get("last_name", "")
    msg = ""
    if (
        usernamebefore != message.from_user.username
        or first_name != message.from_user.first_name
        or lastname_before != message.from_user.last_name
    ):
        msg += f"""User {message.from_user.mention}\n"""
    if usernamebefore != message.from_user.username:
        usernameafter = message.from_user.username or "NO USERNAME"
        msg += """changed her username from {} to {}\n""".format(usernamebefore, usernameafter)
        await add_userdata(
            chat_id,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if first_name != message.from_user.first_name:
        msg += """changed her first name from {} to {}\n""".format(first_name, message.from_user.first_name)
        await add_userdata(
            chat_id,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if lastname_before != message.from_user.last_name:
        lastname_after = message.from_user.last_name or "NO LAST NAME"
        msg += """changed her last name from {} to {}\n""".format(lastname_before, lastname_after)
        await add_userdata(
            chat_id,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if msg != "":
        await message.reply_text(msg)

@app.on_message(filters.group & filters.command("pretender") & ~filters.bot & ~filters.via_bot & admin_filter)
async def set_mataa(_, message: Message):
    if len(message.command) == 1:
        return await message.reply("**Detect pretender usage: /pretender on|off**")
    chat_id = message.chat.id
    if message.command[1] == "on":
        cekset = await check_pretender(chat_id)
        if cekset:
            await message.reply("**Pretender mode is already enabled.**")
        else:
            await impo_on(chat_id)
            await message.reply(f"**Successfully enabled pretender mode for** {message.chat.title}")
    elif message.command[1] == "off":
        cekset = await check_pretender(chat_id)
        if not cekset:
            await message.reply("**Pretender mode is already disabled.**")
        else:
            await impo_off(chat_id)
            await message.reply(f"**Successfully disabled pretender mode for** {message.chat.title}")
    else:
        await message.reply("**Detect pretender users usage: /pretender on|off**")