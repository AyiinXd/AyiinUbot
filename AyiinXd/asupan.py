import os

from random import choice

from fipper import Client, enums
from fipper.types import Message

from pyAyiin import Ayiin, CMD_HELP

from . import *


@Ayiin(["tiktok", "tt"])
async def asupan_cmd(client: Client, message: Message):
    xx = await message.reply("Memproses...")
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


@Ayiin(["bokp", "bkp"])
async def asupan_cmd(client: Client, message: Message):
    xx = await message.reply("Memproses...")
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
            "asupan atau ptl": "Untuk Mengirim video asupan secara random.",
            "bokp atau bkp": "Untuk Mengirim video b*k*p secara random.",
        }
    )
    }
)
