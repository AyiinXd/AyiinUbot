# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-UserBot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-UserBot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio
import os
from io import BytesIO

import cv2
from PIL import Image

from fipper import Client, emoji
from fipper.enums import ParseMode
from fipper.errors import StickersetInvalid, YouBlockedUser
from fipper.raw.functions.messages import GetStickerSet
from fipper.raw.types import InputStickerSetShortName
from fipper.types import Message

from pyAyiin import Ayiin, CMD_HELP
from pyAyiin.pyrogram import eor

from . import *


@Ayiin(["q", "quotly"], langs=True)
async def quotly(client: Client, message: Message, _):
    if not message.reply_to_message:
        return await message.reply_text(_['reply'])
    msg = await message.reply_text(_['p'])
    reply = message.reply_to_message
    cmd = yins.get_cmd(message)
    await msg.delete()
    if reply:
        if cmd.startswith('@') or cmd.isdigit():
            user = await client.get_users(cmd)
            file = await yins.create_quotly(reply, reply=reply, sender=user)
            message = await client.send_sticker(chat_id=message.chat.id, sticker=file)
            os.remove(file)
            return
        else:
            file = await yins.create_quotly(reply)
            message = await client.send_sticker(chat_id=message.chat.id, sticker=file)
            os.remove(file)
            return


@Ayiin(["kang", "tikel"], langs=True)
async def kang(client: Client, message: Message, _):
    user = client.me
    replied = message.reply_to_message
    Ayiin = await eor(message, _['p'])
    media_ = None
    emoji_ = None
    is_anim = False
    is_video = False
    resize = False
    ff_vid = False
    if replied and replied.media:
        if replied.photo:
            resize = True
        elif replied.document and "image" in replied.document.mime_type:
            resize = True
            replied.document.file_name
        elif replied.document and "tgsticker" in replied.document.mime_type:
            is_anim = True
            replied.document.file_name
        elif replied.document and "video" in replied.document.mime_type:
            resize = True
            is_video = True
            ff_vid = True
        elif replied.animation:
            resize = True
            is_video = True
            ff_vid = True
        elif replied.video:
            resize = True
            is_video = True
            ff_vid = True
        elif replied.sticker:
            if not replied.sticker.file_name:
                await Ayiin.edit(_['sticker_1'])
                return
            emoji_ = replied.sticker.emoji
            is_anim = replied.sticker.is_animated
            is_video = replied.sticker.is_video
            if not (
                replied.sticker.file_name.endswith(".tgs")
                or replied.sticker.file_name.endswith(".webm")
            ):
                resize = True
                ff_vid = True
        else:
            await Ayiin.edit("<i>File Tidak Didukung</i>")
            return
        media_ = await client.download_media(replied, file_name="assets/")
    else:
        await Ayiin.edit(_['reply_media'])
        return
    if media_:
        args = yins.get_cmd(message)
        pack = 1
        if len(args) == 2:
            emoji_, pack = args
        elif len(args) == 1:
            if args[0].isnumeric():
                pack = int(args[0])
            else:
                emoji_ = args[0]

        if emoji_ and emoji_ not in (
            getattr(emoji, _) for _ in dir(emoji) if not _.startswith("_")
        ):
            emoji_ = None
        if not emoji_:
            emoji_ = "✨"

        u_name = user.username
        u_name = "@" + u_name if u_name else user.first_name or user.id
        packname = f"Sticker_u{user.id}_v{pack}"
        custom_packnick = f"{u_name} Sticker Pack"
        packnick = f"{custom_packnick} Vol.{pack}"
        cmd = "/newpack"
        if resize:
            media_ = await yins.resize_media(media_, is_video, ff_vid)
        if is_anim:
            packname += "_animated"
            packnick += " (Animated)"
            cmd = "/newanimated"
        if is_video:
            packname += "_video"
            packnick += " (Video)"
            cmd = "/newvideo"
        exist = False
        while True:
            try:
                exist = await client.invoke(
                    GetStickerSet(
                        stickerset=InputStickerSetShortName(short_name=packname), hash=0
                    )
                )
            except StickersetInvalid:
                exist = False
                break
            limit = 50 if (is_video or is_anim) else 120
            if exist.set.count >= limit:
                pack += 1
                packname = f"a{user.id}_by_ayiin_{pack}"
                packnick = f"{custom_packnick} Vol.{pack}"
                if is_anim:
                    packname += f"_anim{pack}"
                    packnick += f" (Animated){pack}"
                if is_video:
                    packname += f"_video{pack}"
                    packnick += f" (Video){pack}"
                await Ayiin.edit(_['sticker_2'].format(pack))
                continue
            break
        if exist is not False:
            try:
                await client.send_message("stickers", "/addsticker")
            except YouBlockedUser:
                await client.unblock_user("stickers")
                await client.send_message("stickers", "/addsticker")
            except Exception as e:
                return await Ayiin.edit(_['err'].format(e))
            await asyncio.sleep(2)
            await client.send_message("stickers", packname)
            await asyncio.sleep(2)
            limit = "50" if is_anim else "120"
            while limit in await get_response(message, client):
                pack += 1
                packname = f"a{user.id}_by_{user.username}_{pack}"
                packnick = f"{custom_packnick} vol.{pack}"
                if is_anim:
                    packname += "_anim"
                    packnick += " (Animated)"
                if is_video:
                    packname += "_video"
                    packnick += " (Video)"
                await Ayiin.edit(_['sticker_2'].format(str(pack)))
                await client.send_message("stickers", packname)
                await asyncio.sleep(2)
                if await get_response(message, client) == "Invalid pack selected.":
                    await client.send_message("stickers", cmd)
                    await asyncio.sleep(2)
                    await client.send_message("stickers", packnick)
                    await asyncio.sleep(2)
                    await client.send_document("stickers", media_)
                    await asyncio.sleep(2)
                    await client.send_message("Stickers", emoji_)
                    await asyncio.sleep(2)
                    await client.send_message("Stickers", "/publish")
                    await asyncio.sleep(2)
                    if is_anim:
                        await client.send_message(
                            "Stickers", f"<{packnick}>", parse_mode=ParseMode.HTML
                        )
                        await asyncio.sleep(2)
                    await client.send_message("Stickers", "/skip")
                    await asyncio.sleep(2)
                    await client.send_message("Stickers", packname)
                    await asyncio.sleep(2)
                    await Ayiin.edit(_['sticker_3'].format(packname))
                    return
            await client.send_document("stickers", media_)
            await asyncio.sleep(2)
            if (
                await get_response(message, client)
                == "Sorry, the file type is invalid."
            ):
                await Ayiin.edit(_['sticker_4'])
                return
            await client.send_message("Stickers", emoji_)
            await asyncio.sleep(2)
            await client.send_message("Stickers", "/done")
        else:
            await Ayiin.edit(_['sticker_5'])
            try:
                await client.send_message("Stickers", cmd)
            except YouBlockedUser:
                await client.unblock_user("stickers")
                await client.send_message("stickers", "/addsticker")
            await asyncio.sleep(2)
            await client.send_message("Stickers", packnick)
            await asyncio.sleep(2)
            await client.send_document("stickers", media_)
            await asyncio.sleep(2)
            if (
                await get_response(message, client)
                == "Sorry, the file type is invalid."
            ):
                await Ayiin.edit(_['sticker_4'])
                return
            await client.send_message("Stickers", emoji_)
            await asyncio.sleep(2)
            await client.send_message("Stickers", "/publish")
            await asyncio.sleep(2)
            if is_anim:
                await client.send_message("Stickers", f"<{packnick}>")
                await asyncio.sleep(2)
            await client.send_message("Stickers", "/skip")
            await asyncio.sleep(2)
            await client.send_message("Stickers", packname)
            await asyncio.sleep(2)
        await Ayiin.edit(_['sticker_3'].format(packname))
        if os.path.exists(str(media_)):
            os.remove(media_)


async def get_response(message, client):
    return [x async for x in client.get_chat_history("Stickers", limit=1)][0].text


@Ayiin(["tiny"], langs=True)
async def tinying(client: Client, message: Message, _):
    reply = message.reply_to_message
    if not (reply and (reply.media)):
        return await eor(message, _['reply_sticker'])
    Xd = await eor(message, _['p'])
    ik = await client.download_media(reply)
    im1 = Image.open("assets/blank.png")
    if ik.endswith(".tgs"):
        await client.download_media(reply, "ayiin.tgs")
        await yins.bash("lottie_convert.py ayiin.tgs json.json")
        json = open("json.json", "r")
        jsn = json.read()
        jsn = jsn.replace("512", "2000")
        ("json.json", "w").write(jsn)
        await yins.bash("lottie_convert.py json.json ayiin.tgs")
        file = "ayiin.tgs"
        os.remove("json.json")
    elif ik.endswith((".gif", ".mp4")):
        iik = cv2.VideoCapture(ik)
        busy = iik.read()
        cv2.imwrite("i.png", busy)
        fil = "i.png"
        im = Image.open(fil)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove(fil)
        os.remove("k.png")
    else:
        im = Image.open(ik)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove("k.png")
    await asyncio.gather(
        Xd.delete(),
        client.send_sticker(
            message.chat.id,
            sticker=file,
            reply_to_message_id=yins.ReplyCheck(message),
        ),
    )
    os.remove(file)
    os.remove(ik)


@Ayiin(["mmf", "memify"], langs=True)
async def memify(client: Client, message: Message, _):
    if not message.reply_to_message_id:
        await eor(message, _['reply_media'])
        return
    reply_message = message.reply_to_message
    if not reply_message.media:
        await eor(message, _['reply_media'])
        return
    file = await client.download_media(reply_message)
    Xd = await eor(message, _['p'])
    text = yins.get_cmd(message)
    if len(text) < 1:
        return await Xd.edit(_['sticker_6'])
    meme = await yins.add_text_img(file, text, "assets/default.ttf")
    await asyncio.gather(
        Xd.delete(),
        client.send_sticker(
            message.chat.id,
            sticker=meme,
            reply_to_message_id=yins.ReplyCheck(message),
        ),
    )
    os.remove(meme)


@Ayiin(["getsticker", "mtoi"], langs=True)
async def stick2png(client: Client, message: Message, _):
    try:
        await message.edit(_['download'])

        path = await message.reply_to_message.download()
        with open(path, "rb") as f:
            content = f.read()
        os.remove(path)

        file_io = BytesIO(content)
        file_io.name = "sticker.png"

        await asyncio.gather(
            message.delete(),
            client.send_photo(
                message.chat.id,
                file_io,
                reply_to_message_id=yins.ReplyCheck(message),
            ),
        )
    except Exception as e:
        return await message.reply(_['err'].format(str(e)))


CMD_HELP.update(
    {"stickers": (
        "stickers",
        {
            "q": "Membuat pesan menjadi sticker dengan random background.",
            "kang": "Balas Ke Sticker Atau Gambar Untuk Menambahkan Ke Sticker Pack.",
            "mmf": "Menambahkan text di sticker.",
            "mtoi": "Mengubah Sticker Menjadi Gambar.",
            "tiny": "Mengubah Ukuran Sticker Menjadi Kecil.",
        }
        )
    }
)