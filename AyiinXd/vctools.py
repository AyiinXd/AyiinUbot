# Ayiin - Ubot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinUbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinUbot/blob/main/LICENSE/>.
#
# FROM AyiinUbot <https://github.com/AyiinXd/AyiinUbot>
# t.me/AyiinChat & t.me/AyiinSupport


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

from fipper.types import Message

from pyAyiin import Ayiin, CMD_HELP, Yins

from . import *


@Ayiin(['startvc'], pass_error=True)
async def start_vcs(client, msg):
    title = yins.get_cmd(msg)
    if title:
        try:
            await Yins.StartVc(client, msg, title)
            await eor(msg, f'Berhasil Memulai Obrolan Suara\n\nChat: {msg.chat.title}\nChat ID: {msg.chat.id}')
        except Exception as e:
            await msg.reply(e)
    try:
        await Yins.StartVc(client, msg)
    except Exception as e:
        await msg.reply(e)


@Ayiin(["stopvc"])
async def end_vc_(client: Client, message: Message):
    """End group call"""
    chat_id = message.chat.id
    await Yins.StopVc(client, message)
    await eor(message, f"<i>Ended group call</i>\n<b>Chat ID:</b> <code>{chat_id}</code>")


CMD_HELP.update(
    {"vctools":(
        "vctools",
        {
            "startvc" : "Memulai obrolan suara.",
            "joinvc" : "Bergabung di obrolan suara.",
        }
    )
    }
)