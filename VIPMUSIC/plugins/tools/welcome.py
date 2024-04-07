from unidecode import unidecode
from PIL import ImageDraw, Image, ImageFont, ImageChops
from pyrogram import *
from pyrogram.types import *
from logging import getLogger
from VIPMUSIC import LOGGER
from VIPMUSIC import app 
import random
import asyncio
from config import LOGGER_ID as LOG_GROUP_ID

#COMMAND_HANDLER = ". /".split()
from async_pymongo import AsyncClient
from config import *



DBNAME = "CUTIEXMUSICBOTss"

mongo = AsyncClient(MONGO_DB_URI)
dbname = mongo[DBNAME]

LOGGER = getLogger(__name__)


wlcm = dbname["welcome"]

async def add_wlcm(chat_id : int):
    return await wlcm.insert_one({"chat_id" : chat_id})

async def rm_wlcm(chat_id : int):   
    chat = await wlcm.find_one({"chat_id" : chat_id})
    if chat: 
        return await wlcm.delete_one({"chat_id" : chat_id})

wlcm = WelDatabase()


class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None

def circle(pfp, size=(450, 450)):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

def welcomepic(pic, user, chat, id, uname):
    background = Image.open("VIPMUSIC/assets/wel1.jpg")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp)
    pfp = pfp.resize(
        (380, 380)
    ) 
    # written by cute bachha 
    draw = ImageDraw.Draw(background)
    # random color s
    c1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    c2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    c3 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    font = ImageFont.truetype('VIPMUSIC/assets/font.ttf', size=50)
    font2 = ImageFont.truetype('VIPMUSIC/assets/font.ttf', size=90)
    draw.text((750, 405), f'{unidecode(user)}', fill=c1, font=font)
    draw.text((650, 500), f'{id}', fill=c2, font=font)
    draw.text((850, 585), f"{uname}", fill=c3, font=font)
    pfp_position = (94, 117)  
    background.paste(pfp, pfp_position, pfp)  
    background.save(
        f"downloads/welcome#{id}.png"
    )
    return f"downloads/welcome#{id}.png"

@app.on_message(filters.command("wel") & ~filters.private)
async def auto_state(_, message):
    usage = "**Usage:**\n/wel [ENABLE|DISABLE]"
    if len(message.command) == 1:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
      A = await wlcm.find_one({"chat_id" : chat_id})
      state = message.text.split(None, 1)[1].strip()
      state = state.lower()
      if state == "enable":
        if A:
           return await message.reply_text("Special Welcome Already Enabled")
        elif not A:
           await add_wlcm(chat_id)
           await message.reply_text(f"Enabled Special Welcome in {message.chat.title}")
      elif state == "disable":
        if not A:
           return await message.reply_text("Special Welcome Already Disabled")
        elif A:
           await rm_wlcm(chat_id)
           await message.reply_text(f"Disabled Special Welcome in {message.chat.title}")
      else:
        await message.reply_text(usage)
    else:
        await message.reply("Only Admins Can Use This Command")

#bhag 

@app.on_chat_member_updated(filters.group, group=-3)
async def greet_group(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    A = await wlcm.find_one({"chat_id" : chat_id})
    if not A:
       return
    if (
        not member.new_chat_member
        or member.new_chat_member.status in {"banned", "left", "restricted"}
        or member.old_chat_member
    ):
        return
    user = member.new_chat_member.user if member.new_chat_member else member.from_user
    try:
        pic = await app.download_media(
            user.photo.big_file_id, file_name=f"pp{user.id}.png"
        )
    except AttributeError:
        pic = "VIPMUSIC/assets/profilepic.jpg"
    if (temp.MELCOW).get(f"welcome-{member.chat.id}") is not None:
        try:
            await temp.MELCOW[f"welcome-{member.chat.id}"].delete()
        except Exception as e:
            LOGGER.error(e)
    try:
        welcomeimg = welcomepic(
            pic, user.first_name, member.chat.title, user.id, user.username
        )
        temp.MELCOW[f"welcome-{member.chat.id}"] = await app.send_photo(
            member.chat.id,
            photo=welcomeimg,
            caption= f"""
**
Name : {user.mention}
┣ 𝐔𝐬ᴇʀɪᴅ : {user.id}
┣ 𝐔𝐬ᴇʀɴᴀᴍᴇ : @{user.username}


""",
reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton (f"hehe", url=f"https//t.me/pokemon")]])
        )
    except Exception as e:
        LOGGER.error(e)
    try:
        os.remove(f"downloads/welcome#{user.id}.png")
        os.remove(f"downloads/pp{user.id}.png")
    except Exception as e:
        pass
