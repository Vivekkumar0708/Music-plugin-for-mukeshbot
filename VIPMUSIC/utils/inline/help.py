
from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from VIPMUSIC import app


def help_pannel(_, START: Union[bool, int] = None):
    first = [InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data=f"close")]
    second = [
        InlineKeyboardButton(
            text="ʙᴀᴄᴋ",
            callback_data=f"settingsback_helper",
        ),
        InlineKeyboardButton(
            text="ᴄʟᴏsᴇ", callback_data=f"close"
        ),
        
    ]
    mark = second if START else first
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ᴀᴅᴍɪɴ",
                    callback_data="help_callback hb1",
                ),
                InlineKeyboardButton(
                    text="ᴀᴜᴛʜ",
                    callback_data="help_callback hb2",
                ),
            
                InlineKeyboardButton(
                    text="ʙʟᴏᴄᴋ",
                    callback_data="help_callback hb3",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="ɢᴄᴀsᴛ",
                    callback_data="help_callback hb4",
                ),
                InlineKeyboardButton(
                    text="ɢʙᴀɴ",
                    callback_data="help_callback hb12",
                ),
                InlineKeyboardButton(
                    text="ᴇxᴛʀᴀ",
                    callback_data="help_callback hb5",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="ᴘʟᴀʏʟɪsᴛ",
                    callback_data="help_callback hb6",
                ),
                InlineKeyboardButton(
                    text="ᴠᴏɪᴄᴇ-ᴄʜᴀᴛ",
                    callback_data="help_callback hb10",
                ),
                InlineKeyboardButton(
                    text="ᴛᴏᴏʟs",
                    callback_data="help_callback hb13",
                ),
            ],
            [
           
                InlineKeyboardButton(
                    text="ᴘʟᴀʏ",
                    callback_data="help_callback hb8",
                ),
            
            
                InlineKeyboardButton(
                    text="sᴜᴅᴏ",
                    callback_data="help_callback hb9",
                ),
                InlineKeyboardButton(
                    text="sᴛᴀʀᴛ",
                    callback_data="help_callback hb11",
                ),
            ],
            
            mark,
        ]
    )
    return upl


def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ʙᴀᴄᴋ",
                    callback_data=f"settings_back_helper",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="ᴄʟᴏsᴇ", callback_data=f"close"
                ),
                

            ]
        ]
    )
    return upl


def fun_page():
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ʙᴀᴄᴋ",
                    callback_data=f"settings_back_helper",
                ),
            ],
            
        ]
    )
    return upl


def private_help_panel(_):
    buttons = [
             
             [
            InlineKeyboardButton(text="ᴏᴘᴇɴ ʜᴇʀᴇ", callback_data="settings_back_helper")
        ],
             [
            InlineKeyboardButton(text="ᴏᴘᴇɴ ɪɴ ᴘʀɪᴠᴀᴛᴇ ", url=f"https://t.me/{app.username}?start=mhelp"),
        ],


    ]
    return buttons
