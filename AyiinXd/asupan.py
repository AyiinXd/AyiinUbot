# Ayiin - Userbot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/Ayiin-Userbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/Ayiin-Userbot/blob/main/LICENSE/>.
#
# FROM Ayiin-Userbot <https://github.com/AyiinXd/Ayiin-Userbot>
# t.me/AyiinXdSupport & t.me/AyiinChannel


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import os

from random import choice

from fipper import Client, enums
from fipper.types import Message

from config import Var
from pyAyiin import Ayiin, BLACKLIST_CHAT, CMD_HELP

from . import *


@Ayiin(["asupan", "asp"], langs=True)
async def asupan_cmd(client: Client, message: Message, _):
    if message.chat.id in BLACKLIST_CHAT:
        return await message.reply(_["ayiin_1"])
    xx = await message.reply(_['p'])
    asupannya = [
        asupan
        async for asupan in message.client.search_messages(
            "tedeasupancache", filter=enums.MessagesFilter.VIDEO
        )
    ]
    file = await message.client.download_media(choice(asupannya), "./tiktok/")
    await message.client.send_video(
        chat_id=message.chat.id,
        video=file,
        reply_to_message_id=yins.ReplyCheck(message)
    )
    await xx.delete()
    os.remove(file)


@Ayiin(["bokp", "bkp"], langs=True)
async def asupan_cmd(client: Client, message: Message, _):
    if message.chat.id in BLACKLIST_CHAT:
        return await message.reply(_["ayiin_1"])
    xx = await message.reply(_['p'])
    asupannya = [
        asupan
        async for asupan in message.client.search_messages(
            "bkpxd1001756067648", filter=enums.MessagesFilter.VIDEO
        )
    ]
    file = await message.client.download_media(choice(asupannya), "./bokp/")
    await message.client.send_video(
        chat_id=message.chat.id,
        video=file,
        reply_to_message_id=yins.ReplyCheck(message)
    )
    await xx.delete()
    os.remove(file)


CMD_HELP.update(
    {"asupan": (
        "asupan",
        {
            "tiktok atau tt": "Untuk Mengirim video asupan secara random.",
            "bokp atau bkp": "Untuk Mengirim video b*k*p secara random.",
        }
    )
    }
)
