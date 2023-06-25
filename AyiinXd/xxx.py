import os
import requests
import urllib

from fipper import Client
from fipper.types import Message
from fipper.errors import ChatSendMediaForbidden
from pyAyiin import BLACKLIST_CHAT, CMD_HELP
from pyAyiin.decorator import Ayiin

from . import *


@Ayiin(['boob', 'tete'], langs=True)
async def search_anu(client: Client, message: Message, _):
    if message.chat.id in BLACKLIST_CHAT:
        return await message.reply(_["ayiin_1"])
    if not os.path.isdir('./file_tt/'):
        os.makedirs('./file_tt/')
    pic_loc = os.path.join('./file_tt/', "bobs.jpg")
    a = await message.reply(_["x_1"])
    nsfw = requests.get("http://api.oboobs.ru/noise/1").json()[0]["preview"]
    urllib.request.urlretrieve(
        "http://media.oboobs.ru/{}".format(nsfw), pic_loc)
    try:
        await client.send_photo(
            message.chat.id,
            pic_loc,
            caption=_["x_2"],
            reply_to_message_id=yins.ReplyCheck(message),
        )
        os.remove(pic_loc)
        return
    except ChatSendMediaForbidden:
        return await message.reply(_["err_media"])


CMD_HELP.update(
    {"xxx":(
        "xxx",
        {
            "xxx": "Untuk mendapatkan gambar payudara",
        }
    )
    }
)