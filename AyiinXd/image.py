# Ayiin - Userbot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/Ayiin-Userbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/Ayiin-Userbot/blob/main/LICENSE/>.
#
# FROM Ayiin-Userbot <https://github.com/AyiinXd/Ayiin-Userbot>
# t.me/AyiinXdSupport & t.me/AyiinSupport


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import asyncio
import cv2
import io
import os
import requests

from fipper import Client, raw
from fipper.types import Message

from pyAyiin import CMD_HELP
from pyAyiin.decorator import Ayiin
from pyAyiin.pyrogram import eor

from config import Var

from . import yins


@Ayiin(["rbg", "removebg", "remove_bg"])
async def kbg(client: Client, message: Message):
    if Var.REM_BG_API_KEY is None:
        await eor(
            message,
            "Remove.Bg Api Token hilang! Tambahkan ke vars Heroku atau .env."
        )
        return
    if message.reply_to_message:
        message.reply_to_message.id
        reply_message = message.reply_to_message
        xx = await eor(message, "<i>Memproses...</i>")
        try:
            if isinstance(
                reply_message.media, raw.types.MessageMediaPhoto
            ) or reply_message.media:
                downloaded_file_name = await client.download_media(
                    reply_message,
                    Var.TEMP_DOWNLOAD_DIRECTORY
                )
                await xx.edit("<i>Menghapus latar belakang dari gambar ini...</i>")
                output_file_name = await ReTrieveFile(downloaded_file_name)
                os.remove(downloaded_file_name)
            else:
                await xx.edit("<i>Bagaimana cara menghapus latar belakang ini ?</i>")
        except Exception as e:
            await xx.edit(f"ERROR: {(str(e))}")
            return
        try:
            client.me = await client.get_me()
        except BaseException:
            pass
        contentType = output_file_name.headers.get("content-type")
        if "image" in contentType:
            with io.BytesIO(output_file_name.content) as remove_bg_image:
                remove_bg_image.name = "AyiinBg.png"
                await client.send_document(
                    message.chat.id,
                    document=remove_bg_image,
                    force_document=True,
                    reply_to_message_id=yins.ReplyCheck(message),
                )
                await xx.delete()
        else:
            await xx.edit(
                "<b>Kesalahan (Kunci API tidak valid, saya kira ?)</b>\n<i>{}</i>".format(
                    output_file_name.content.decode("UTF-8")
                ),
            )
    else:
        return await message.reply("Silahkan Balas Ke Gambar")


# this method will call the API, and return in the appropriate format
# with the name provided.
async def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": Var.REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )


async def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": Var.REM_BG_API_KEY,
    }
    data = {"image_url": input_url}
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True,
    )


@Ayiin(["blur"])
async def blur_image(client: Client, message: Message):
    ureply = message.reply_to_message
    xd = await message.reply("<i>Memproses...</i>")
    if not ureply.media:
        return await xd.edit("Balas Ke Gambar Ngentod")

    yinsxd = await client.download_media(ureply, Var.TEMP_DOWNLOAD_DIRECTORY)
    if yinsxd.endswith(".tgs"):
        cmd = ["lottie_convert.py", yinsxd, "yin.png"]
        file = "yin.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    else:
        img = cv2.VideoCapture(yins)
        heh, lol = img.read()
        cv2.imwrite("yin.png", lol)
        file = "yin.png"
    yin = cv2.imread(file)
    ayiinxd = cv2.GaussianBlur(yin, (35, 35), 0)
    cv2.imwrite("yin.jpg", ayiinxd)
    await client.send_photo(
        message.chat.id,
        "yin.jpg",
        reply_to_message_id=yins.ReplyCheck(message),
    )
    await xd.delete()
    os.remove("yin.png")
    os.remove("yin.jpg")
    os.remove(yinsxd)


@Ayiin(["negative"])
async def yinsxd(client: Client, message: Message):
    ureply = message.reply_to_message
    ayiin = await message.reply("Memproses...")
    if not ureply.media:
        return await ayiin.edit("Balas Ke Gambar Ngentod")

    ayiinxd = await client.download_media(ureply, Var.TEMP_DOWNLOAD_DIRECTORY)
    if ayiinxd.endswith(".tgs"):
        cmd = ["lottie_convert.py", ayiinxd, "yin.png"]
        file = "yin.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    else:
        img = cv2.VideoCapture(ayiinxd)
        heh, lol = img.read()
        cv2.imwrite("yin.png", lol)
        file = "yin.png"
    yinsex = cv2.imread(file)
    kntlxd = cv2.bitwise_not(yinsex)
    cv2.imwrite("yin.jpg", kntlxd)
    await client.send_photo(
        message.chat.id,
        "yin.jpg",
        reply_to_message_id=yins.ReplyCheck(message),
    )
    await ayiin.delete()
    os.remove("yin.png")
    os.remove("yin.jpg")
    os.remove(ayiinxd)


@Ayiin(["miror"])
async def kntl(client: Client, message: Message):
    ureply = message.reply_to_message
    kentu = await message.reply("<i>Memproses</i>")
    if not ureply.media:
        return await kentu.edit("Balas Ke Gambar Tod")

    xnxx = await client.download_media(ureply, Var.TEMP_DOWNLOAD_DIRECTORY)
    if xnxx.endswith(".tgs"):
        cmd = ["lottie_convert.py", xnxx, "yin.png"]
        file = "yin.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    else:
        img = cv2.VideoCapture(xnxx)
        kont, tol = img.read()
        cv2.imwrite("yin.png", tol)
        file = "yin.png"
    yin = cv2.imread(file)
    mmk = cv2.flip(yin, 1)
    ayiinxd = cv2.hconcat([yin, mmk])
    cv2.imwrite("yin.jpg", ayiinxd)
    await client.send_photo(
        message.chat.id,
        "yin.jpg",
        reply_to_message_id=yins.ReplyCheck(message),
    )
    await kentu.delete()
    os.remove("yin.png")
    os.remove("yin.jpg")
    os.remove(xnxx)


CMD_HELP.update(
    {"image": (
        "image",
        {
            "blur": "Memberika Efek Blur Ke Gambar",
            "miror": "Memberikan Efek Cermin Ke Gambar",
            "negative": "Memberikan Efek Negative Ke Gambar",
            "rbg": "Menghapus Latar Belakang Gambar",
        }
    )
    }
)
