from io import BytesIO
from random import randint
from secrets import choice
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont
from requests import get

from fipper import Client
from fipper.types import Message

from pyAyiin import Ayiin, CMD_HELP

from . import *


@Ayiin(["imp", "impostor"])
async def f_load(client: Client, message: Message):
    clrs = {
        "red": 1,
        "lime": 2,
        "green": 3,
        "blue": 4,
        "cyan": 5,
        "brown": 6,
        "purple": 7,
        "pink": 8,
        "orange": 9,
        "yellow": 10,
        "white": 11,
        "black": 12,
    }
    clr = randint(1, 12)
    text = yins.get_cmd(message)
    reply = message.reply_to_message
    if text in clrs:
        clr = clrs[text]
        text = None
    if not text:
        if not reply:
            await bruh(message, message.from_user)
            return
        if not reply.text:
            await bruh(message, reply.from_user)
            return
        text = reply.text.split(" ", 1)[1]
    if text.split(" ")[0] in clrs:
        clr = clrs[text.split(" ")[0]]
        text = " ".join(text.split(" ")[1:])
    if text == "colors":
        await message.edit(
            ("Cores disponíveis:\n" + "\n".join(f"• `{i}`" for i in list(clrs.keys())))
        )
        return
    url = "https://raw.githubusercontent.com/KeyZenD/AmongUs/master/"
    font = ImageFont.truetype(BytesIO(get(url + "bold.ttf").content), 60)
    imposter = Image.open(BytesIO(get(f"{url}{clr}.png").content))
    text_ = "\n".join("\n".join(wrap(part, 30)) for part in text.split("\n"))
    w, h = ImageDraw.Draw(Image.new("RGB", (1, 1))).multiline_textsize(
        text_, font, stroke_width=2
    )
    text = Image.new("RGBA", (w + 30, h + 30))
    ImageDraw.Draw(text).multiline_text(
        (15, 15), text_, "#FFF", font, stroke_width=2, stroke_fill="#000"
    )
    w = imposter.width + text.width + 10
    h = max(imposter.height, text.height)
    image = Image.new("RGBA", (w, h))
    image.paste(imposter, (0, h - imposter.height), imposter)
    image.paste(text, (w - text.width, 0), text)
    image.thumbnail((512, 512))
    output = BytesIO()
    output.name = "imposter.webp"
    image.save(output)
    output.seek(0)
    await message.delete()
    await message.reply_sticker(
        sticker=output,
        reply_to_message_id=yins.ReplyCheck(message),
    )



async def bruh(message, user):
    fn = user.first_name
    ln = user.last_name
    name = fn + (" " + ln if ln else "")
    name = "***" + name
    await message.edit(name + choice([" ", " Tidak "]) + "Adalah Seorang Penipu! ***")


CMD_HELP.update(
    {"amongus": (
        "amongus",
        {
          "imp": "Berikan Teks Untuk Membuat Sticker Among Us",
        }
    )
      
    }
)
