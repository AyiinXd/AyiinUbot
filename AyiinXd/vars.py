

from fipper.types import Message

from pyAyiin import CMD_HELP
from pyAyiin.dB.variable import del_var, get_var, set_var
from pyAyiin.decorator import Ayiin

from . import *


@Ayiin(["set_var"], langs=True)
async def setdv_handler(client, m: Message, _):
    cmd = m.command[1]
    value = m.text.split(None, 2)[2]
    if not cmd and not value:
        return await m.reply(_["vars_1"])
    else:
        await set_var(cmd, value)
        return await m.reply(_["vars_2"].format(cmd, value))


@Ayiin(["del_var"], langs=True)
async def deldv_handler(client, m: Message, _):
    cmd = yins.get_cmd(m)
    if not cmd:
        return await m.reply(_["vars_3"])
    else:
        await del_var(cmd)
        return await m.reply(_["vars_4"].format(cmd))


@Ayiin(["get_var"], langs=True)
async def getdv_handler(client, m: Message, _):
    cmd = yins.get_cmd(m)
    if not cmd:
        return await m.reply(_["vars_5"])
    else:
        done = await get_var(cmd)
        if done:
            return await m.reply(_["vars_6"].format(cmd, done))
        else:
            return await m.reply(_["vars_7"])


CMD_HELP.update(
    {"vars": (
        "vars",
        {
            "set_var [variable, value]": "Set vars database.",
            "del_var [variable]": "Untuk menghapus vars database.",
            "get_var [variable]": "Untuk mendapatkan vars database.",
        }
    )
    }
)