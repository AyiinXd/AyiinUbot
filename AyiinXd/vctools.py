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

from time import sleep
from contextlib import suppress

from pyAyiin import Ayiin, CMD_HELP, Yins

from . import *


@Ayiin(['startvc'], group_only=True, langs=True)
async def start_vcs(client, msg, _):
    xd = await eor(msg, _["vctol_1"])
    title = yins.get_cmd(msg)
    if title:
        try:
            await Yins.StartVc(client, msg, title)
            await xd.edit(_["vctol_2"].format(title, msg.chat.title, msg.chat.id))
        except Exception as e:
            await msg.reply(e)
    else:
        try:
            await Yins.StartVc(client, msg)
            await xd.edit(_["vctol_3"].format(msg.chat.title, msg.chat.id))
        except Exception as e:
            await msg.reply(e)


@Ayiin(["stopvc"], group_only=True, langs=True)
async def end_vc_(client: Client, message: Message, _):
    """End group call"""
    chat_id = message.chat.id
    await Yins.StopVc(client, message)
    await eor(message, _["vctol_4"].format(chat_id))


@Ayiin(["joinvcs", "jovcs"], group_only=True, devs=True)
@Ayiin(["joinvc"], group_only=True, langs=True)
async def joinvc(client: Client, message: Message, _):
    chat_id = message.command[1] if len(
        message.command) > 1 else message.chat.id
    xx = await message.reply(_["p"])
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.group_call.start(chat_id)
    except Exception as e:
        return await xx.edit(_["err"].format(e))
    await xx.edit(_["vctol_5"].format(client.me.mention, chat_id))
    sleep(5)
    try:
        await client.group_call.set_is_mute(True)
    except:
        sleep(5)
        await client.group_call.set_is_mute(True)
    finally:
        pass


@Ayiin(["leavevcs", "levcs"], group_only=True, devs=True)
@Ayiin(["leavevc", "lvc"], group_only=True, langs=True)
async def leavevc(client: Client, message: Message, _):
    chat_id = message.command[1] if len(
        message.command) > 1 else message.chat.id
    xx = await message.reply(_["p"])
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.group_call.stop()
    except Exception as e:
        return await message.reply(_["err"].format(e))
    else:
        await xx.edit(_['vctol_6'].format(client.me.mention, chat_id))


CMD_HELP.update(
    {"vctools":(
        "vctools",
        {
            "startvc": "Memulai Obrolan Suara Digrup",
            "stopvc": "Mengakhiri Obrolan Suara Digrup",
            "joinvc": "Bergabung Ke Obrolan Suara Digrup",
            "leavevc": "Meninggalkan Obrolan Suara Digrup",
        }
    )
    }
)