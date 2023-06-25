# Copyright (C) 2020  sandeep.n(π.$)
# button post makker for catuserbot thanks to uniborg for the base
# by @sandy1709 (@mrconfused)
#
# Recode By : @AyiinXd


import os
import re

from fipper import Client
from fipper.enums import ParseMode
from fipper.types import *

from pyAyiin import CMD_HELP, tgbot
from pyAyiin.decorator import Ayiin
from pyAyiin.pyrogram import eod


from . import *

# regex obtained from:
# https://github.com/PaulSonOfLars/tgbot/blob/master/tg_bot/modules/helper_funcs/string_handling.py#L23
BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")


@Ayiin(["button"])
async def c_button(client: Client, msg: Message):
    reply_message = msg.reply_to_message
    if reply_message:
        markdown_note = reply_message.text
    else:
        markdown_note = "".join(msg.text.split(maxsplit=1)[1:])
    if not markdown_note:
        return await eod(
            msg, "**Teks apa yang harus saya gunakan di pesan button?**"
        )
    prev = 0
    note_data = ""
    buttons = []
    for match in BTN_URL_REGEX.finditer(markdown_note):
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and markdown_note[to_check] == "\\":
            n_escapes += 1
            to_check -= 1
        if n_escapes % 2 == 0:
            buttons.append((match.group(2), match.group(3), bool(match.group(4))))
            note_data += markdown_note[prev : match.start(1)]
            prev = match.end(1)
        elif n_escapes % 2 == 1:
            note_data += markdown_note[prev:to_check]
            prev = match.start(1) - 1
        else:
            break
    else:
        note_data += markdown_note[prev:]
    message_text = note_data.strip() or None
    tl_ib_buttons = build_keyboard(buttons)
    tgbot_reply_message = None
    if reply_message and reply_message.media:
        tgbot_reply_message = await msg.client.download_media(reply_message.media)
    if tl_ib_buttons == []:
        tl_ib_buttons = None
    await tgbot.send_message(
        chat_id=msg.chat.id,
        text=message_text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=False,
        reply_markup=InlineKeyboardMarkup(tl_ib_buttons),
    )
    await msg.delete()
    if tgbot_reply_message:
        await tgbot.send_document(
            chat_id=msg.chat_id,
            caption=message_text,
            parse_mode=ParseMode.HTML,
            document=tgbot_reply_message,
            disable_web_page_preview=False,
            reply_markup=InlineKeyboardMarkup(tl_ib_buttons),
        )
        os.remove(tgbot_reply_message)


def build_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn[2] and keyb:
            keyb[-1].append(InlineKeyboardButton(btn[0], url=btn[1]))
        else:
            keyb.append([InlineKeyboardButton(btn[0], url=btn[1])])
    return keyb


CMD_HELP.update(
    {"button": (
        "button",
        {
            "button" : "Untuk membuat pesan button\n\nNOTE: Bot harus ditambahkan ke group atau channel untuk menggunakan modul ini\n\n**Contoh :** `.cbutton test\n[google]<buttonurl:https://www.google.com>\n[Channel]<buttonurl:https://t.me/AyiinChannel:same>\n[Support]<buttonurl:https://t.me/AyiinChats>`",
        }
    )
    }
)