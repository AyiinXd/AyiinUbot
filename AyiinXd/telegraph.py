# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-UserBot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-UserBot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import os

from fipper import Client
from fipper.types import Message
from telegraph import Telegraph, exceptions, upload_file

from pyAyiin import Ayiin, CMD_HELP

from . import *


telegraph = Telegraph()
r = telegraph.create_account(short_name="AyiinUbot")
auth_url = r["auth_url"]


@Ayiin(["tg", "telegraph"], langs=True)
async def uptotelegraph(client: Client, message: Message, _):
    if not message.reply_to_message:
        return await message.reply(_['reply_media'])
    if message.reply_to_message.media:
        m_d = await message.reply_to_message.download()
        try:
            media_url = upload_file(m_d)
        except exceptions.TelegraphException as exc:
            await message.reply(_['err'].format(exc))
            os.remove(m_d)
            return
        else:
            await message.reply(_['telegraph'].format(media_url[0]))
        os.remove(m_d)
    elif message.reply_to_message.text:
        page_title = yins.get_text(message) if yins.get_text(
            message) else client.me.first_name
        page_text = message.reply_to_message.text
        page_text = page_text.replace("\n", "<br>")
        try:
            response = telegraph.create_page(
                page_title, html_content=page_text)
        except exceptions.TelegraphException as exc:
            return await message.reply(_['err'].format(exc))
        await message.reply(_['telegraph'].format(response['path']))


CMD_HELP.update(
    {"telegraph": (
        "telegraph",
        {
            "tg": "Balas ke Pesan Teks atau Media untuk mengunggahnya ke telegraph.",
        }
    )
    }
)
