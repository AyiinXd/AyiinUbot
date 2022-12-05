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

import time

from datetime import datetime

from fipper import Client
from fipper.types import Message

from pyAyiin import CMD_HELP
from pyAyiin.decorator import Ayiin

from . import *


@Ayiin(["ping", "yins"])
async def pingme(client: Client, message: Message):
    start = datetime.now()
    uptime = await yins.get_readable_time((time.time() - StartTime))
    xnxx = await message.reply("<b>✧</b>")
    await xnxx.edit("<b>✧✧</b>")
    await xnxx.edit("<b>✧✧✧</b>")
    await xnxx.edit("<b>✧✧✧✧</b>")
    await xnxx.edit("<b>✧✧✧✧✧</b>")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await xnxx.edit(
        f"<b>✧ Aʏɪɪɴ Uʙᴏᴛ ✧</b>\n\n"
        f"<b>✧ Pɪɴɢᴇʀ :</b> <code>{duration}ms</code>\n"
        f"<b>✧ Uᴘᴛɪᴍᴇ :</b> <code>{uptime}</code>"
    )


CMD_HELP.update(
    {"ping": (
        "ping",
        {
            "ping": "Check Ping Your Bot.",
        }
    )
    }
)
