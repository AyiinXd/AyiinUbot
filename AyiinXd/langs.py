# Ayiin - Ubot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinUbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinUbot/blob/main/LICENSE/>.
#
# FROM AyiinUbot <https://github.com/AyiinXd/AyiinUbot>
# t.me/AyiinChats & t.me/AyiinChannel


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

from fipper import Client
from fipper.types import Message

from pyAyiin import Ayiin, CMD_HELP
from pyAyiin.Clients.client import tgbot

from . import *


@Ayiin(["lang"], langs=True)
async def set_lang(client: Client, message: Message, _):
    try:
        tgbot.me = await tgbot.get_me()
        results = await client.get_inline_bot_results(tgbot.me.username, f"langs_{client.me.id}")
        await message.reply_inline_bot_result(
            results.query_id,
            results.results[0].id,
            reply_to_message_id=yins.ReplyCheck(message),
        )
    except BaseException as e:
        await message.reply(_["err"].format(e))


CMD_HELP.update(
    {"langs": (
        "langs",
        {
            "lang": "Pilih bahasa yang ingin anda gunakan.",
        }
        )
    }
)