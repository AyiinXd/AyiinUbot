
from fipper import Client
from fipper.types import Message

from pyAyiin import Ayiin, CMD_HELP

from . import *


@Ayiin(["tt", "tiktok"], langs=True)
async def tiktok_dl(client: Client, message: Message, _):
    try:
        xx = await message.reply(_["p"])
        cmd = yins.get_cmd(message)
        if not cmd:
            return await xx.edit(_["link"])
        tiktoker = await yins.tiktok_downloader(cmd)
        try:
            await message.reply_video(
                video=tiktoker,
                caption=_["tiktok_1"].format(client.me.mention),
                reply_to_message_id=yins.ReplyCheck(message)
            )
            await xx.delete()
        except:
            await xx.edit(_["err_media"])
    except BaseException as e:
        await message.reply(_["tiktok_2"])


CMD_HELP.update(
    {"tiktok": (
        "tiktok",
        {
            "tt" : "Untuk Mendownload Video Tiktok.",
        }
    )
    }
)
