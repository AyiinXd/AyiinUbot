# Ayiin - Userbot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/Ayiin-Userbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/Ayiin-Userbot/blob/main/LICENSE/>.
#
# FROM Ayiin-Userbot <https://github.com/AyiinXd/Ayiin-Userbot>
# t.me/AyiinXdSupport & t.me/AyiinSupport


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import os
import re

import aiofiles
from fipper import Client
from fipper.types import Message
from random import choice

from pyAyiin import Ayiin, CMD_HELP, tgbot
from pyAyiin.pyrogram import eor

from . import *



@Ayiin(["paste", "pst"])
async def paste_func(client: Client, message: Message):
    if not message.reply_to_message:
        return await eor(message, f"Balas Chat Dengan Perintah {choice(hndlr)}paste")
    r = message.reply_to_message
    if not r.text and not r.document:
        return await eor(message, "Hanya Text Dan Document Yang Bisa Saya Paste.")
    m = await eor(message, "<code>Pasting...</code>")
    if r.text:
        content = str(r.text)
    elif r.document:
        if r.document.file_size > 40000:
            return await m.edit("Anda hanya dapat menempelkan file yang lebih kecil dari 40KB.")
        pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")
        if not pattern.search(r.document.mime_type):
            return await m.edit("Hanya file teks yang dapat ditempel.")
        doc = await message.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()
        os.remove(doc)
    done, key = await yins.get_paste(content)
    if not done:
        return await m.edit(key)
    link = f"https://spaceb.in/{key}"
    raw = f"https://spaceb.in/api/v1/documents/{key}/raw"
    try:
        if tgbot:
            try:
                tgbot.me = await tgbot.get_me()
                results = await client.get_inline_bot_results(tgbot.me.username, f"paste-{key}")
                await message.reply_inline_bot_result(
                    results.query_id,
                    results.results[0].id,
                    reply_to_message_id=yins.ReplyCheck(message),
                )
            except BaseException as e:
                await m.edit(e)
        else:
            await message.reply_photo(
                photo=link,
                quote=False,
                caption=f"• <b>Pasted to SpaceBin :</b> <a href='{link}'>SpaceBin</a>'\n• <b>Raw Url :</b> <a href='{raw}'>Raw</a>",
            )
        await m.delete()
    except BaseException as e:
        await m.edit(f"<b>ERROR:</b>\n<code>{str(e)}</code>")


CMD_HELP.update(
    {"paste": (
        "paste",
        {
            "paste": "Untuk Menyimpan text ke ke layanan pastebin.",
        }
    )
    }
)