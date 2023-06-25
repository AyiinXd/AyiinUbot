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

from pyAyiin import CMD_HELP, tgbot
from pyAyiin.decorator import Ayiin

from . import *


@Ayiin(["ping"], langs=True)
async def pingme(client: Client, message: Message, _):
    if tgbot:
        try:
            xnxx = await message.reply("<b>✧</b>")
            await xnxx.edit("<b>✧✧</b>")
            await xnxx.edit("<b>✧✧✧</b>")
            await xnxx.edit("<b>✧✧✧✧</b>")
            await xnxx.edit("<b>✧✧✧✧✧</b>")
            tgbot.me = await tgbot.get_me()
            results = await client.get_inline_bot_results(tgbot.me.username, "ping")
            await message.reply_inline_bot_result(
                results.query_id,
                results.results[0].id,
                reply_to_message_id=yins.ReplyCheck(message),
            )
            await xnxx.delete()
        except BaseException as e:
            await eod(xnxx, _['err'].format(e))


CMD_HELP.update(
    {"ping": (
        "ping",
        {
            "ping": "Check Ping Your Bot.",
        }
    )
    }
)
