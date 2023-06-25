from fipper import filters
from fipper.types import *

from pyAyiin import Ayiin, CMD_HELP, listen
from pyAyiin.dB.logdb import add_grup_off, add_grup_on, add_pm_off, add_pm_on, is_grup_logs, is_pm_logs

from . import *


PMLOG = 1
GRUPLOG = 1


@Ayiin(["log"], langs=True)
async def pmlogs(client, message, _):
    command = message.command[1]
    arg = message.text.split(None, 2)[2]
    if not arg:
        await message.reply(_["log_1"])
        return
    if command == "pm":
        if arg == "off":
            await add_pm_off(PMLOG)
            await message.reply(_['log_2'])
        if arg == "on":
            await add_pm_on(PMLOG)
            await message.reply(_['log_3'])
    if command == "gc":
        if arg == "off":
            await add_grup_off(GRUPLOG)
            await message.reply(_['log_4'])
        if arg == "on":
            await add_grup_on(GRUPLOG)
            await message.reply(_['log_5'])
    if command == "all":
        if arg == "off":
            await add_grup_off(GRUPLOG)
            await add_pm_off(PMLOG)
            await message.reply(_['log_6'])
        if arg == "on":
            await add_grup_on(GRUPLOG)
            await add_pm_on(PMLOG)
            await message.reply(_['log_7'])
    if command not in ["pm", "gc", "all"]:
        return await message.reply(_['log_8'])


@listen(
    filters.private
    & filters.incoming
    & ~filters.service
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
)
async def pmlogchat(client, message):
    if await is_pm_logs(PMLOG):
        chat = message.chat.id
        async for pepek in client.search_messages(chat, limit=1):
            await yins.logger_bot(client=client, pepek=pepek)


@listen(filters.mentioned & filters.incoming & filters.group)
async def grouplogchat(client, message):
    if await is_grup_logs(GRUPLOG):
        await yins.logger_bot(client, message, True)


CMD_HELP.update(
    {"log": (
        "log",
        {
            "log [pm/gc/all] [on/off]" : "Untuk mengaktifkan log userbot atau mematikan log userbot.\n\nNotes:\nPm: Personal Message\nGc: Group Chat\nAll: Group Chat and Personal Message\n\nExample:\n.log pm on/off",
        }
    ) 
    }
)