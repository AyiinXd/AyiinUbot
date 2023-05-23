#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import io
import traceback
import sys
import os
import os.path
import random
import re
import subprocess
import time
from os.path import exists, isdir
from natsort import os_sorted

from io import StringIO
from pybase64 import b64decode, b64encode
from fipper import Client
from fipper.types import Message

from config import Var
from pyAyiin import Ayiin, CMD_HELP

from . import *


async def aexec(code, client, message):
    exec(
        f"async def __aexec(client, message): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@Ayiin(["Ev", "Eval"], devs=True)
async def evaluate(client, message: Message):
    Ayiin = await eor(message, "<code>Running ...</code>")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        await Ayiin.delete()
        return
    message.id
    if message.reply_to_message:
        message.reply_to_message_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"<b>Command:</b>\n<code>{cmd}</code>\n\n<b>OUTPUT:</b>\n<code>{evaluation.strip()}</code>"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await message.reply_document(
            document=filename,
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=yins.ReplyCheck(message),
        )
        os.remove(filename)
        await Ayiin.delete()
    else:
        await Ayiin.edit(final_output)


@Ayiin(["Sh", "Bash"], devs=True)
async def terminal(client: Client, message):
    if len(message.text.split()) == 1:
        await message.edit(f"Usage: <code>{Var.HNDLR}bash echo owo</code>")
        return
    args = message.text.split(None, 1)
    teks = args[1]
    if "\n" in teks:
        code = teks.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
            except Exception as err:
                print(err)
                await message.edit(
                    """
<b>Error:</b>
<code>{}</code>
""".format(
                        err
                    )
                )
            output += "<b>{}</b>\n".format(code)
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", teks)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type, value=exc_obj, tb=exc_tb
            )
            await message.edit("""<b>Error:</b>\n<code>{}</code>""".format("".join(errors)))
            return
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await client.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=yins.ReplyCheck(message),
                caption="<code>Output file</code>",
            )
            os.remove("output.txt")
            return
        else:
            await message.edit(f"<b>Output:</code>\n<code>{output}</code>")
    else:
        await message.edit("<b>Output:</code>\n<code>No Output</code>")


@Ayiin(["B64", "Base64"], devs=True)
async def base64(client: Client, message: Message):
    argv = yins.get_cmd(message)
    args = argv.split(" ", 1)
    if len(args) < 2 or args[0] not in ["en", "de"]:
        await message.reply_text(f"<b>Gunakan</b> <code>{Var.HNDLR}b64</code> <code>en</code> <b>atau</b> <code>de</code>")
        return
    args[1] = args[1].replace("`", "")
    if args[0] == "en":
        lething = str(b64encode(bytes(args[1], "utf-8")))[2:]
        await message.reply_text(f"<b>Input:</b> <code>{args[1]}</code>\n\n<b>Encoded:</b> <code>{lething[:-1]}</code>")
    else:
        lething = str(b64decode(bytes(args[1], 'utf-8')))[2:]
        await message.reply_text(f"<b>Input:</b> <code>{args[1]}</code>\n\n<b>Decoded:</b> <code>{lething[:-1]}</code>")


MAX_MESSAGE_SIZE_LIMIT = 4095


@Ayiin(["ls"], devs=True)
async def lst(client, message: Message):
    cat = yins.get_cmd(message)
    path = cat or os.getcwd()
    if not exists(path):
        await message.reply(
            f"Tidak ada direktori atau file dengan nama <code>{cat}</code> coba check lagi!"
        )
        return
    if isdir(path):
        if cat:
            msg = f"<b>Folder dan File di</b> <code>{path}</code> :\n\n"
        else:
            msg = "<b>Folder dan File di Direktori Saat Ini</b> :\n\n"
        lists = os.listdir(path)
        files = ""
        folders = ""
        for contents in os_sorted(lists):
            catpath = path + "/" + contents
            if not isdir(catpath):
                size = os.stat(catpath).st_size
                if contents.endswith((".mp3", ".flac", ".wav", ".m4a")):
                    files += "🎵 "
                elif contents.endswith((".opus")):
                    files += "🎙 "
                elif contents.endswith(
                    (".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")
                ):
                    files += "🎞 "
                elif contents.endswith(
                    (".zip", ".tar", ".tar.gz", ".rar", ".7z", ".xz")
                ):
                    files += "🗜 "
                elif contents.endswith(
                    (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico", ".webp")
                ):
                    files += "🖼 "
                elif contents.endswith((".exe", ".deb")):
                    files += "⚙️ "
                elif contents.endswith((".iso", ".img")):
                    files += "💿 "
                elif contents.endswith((".apk", ".xapk")):
                    files += "📱 "
                elif contents.endswith((".py")):
                    files += "🐍 "
                else:
                    files += "📄 "
                files += f"<code>{contents}</code> (<i>{yins.humanbytes(size)}</i>)\n"
            else:
                folders += f"📁 <code>{contents}</code>\n"
        msg = msg + folders + files if files or folders else msg + "<i>empty path</i>"
    else:
        size = os.stat(path).st_size
        msg = "Rincian file yang diberikan:\n\n"
        if path.endswith((".mp3", ".flac", ".wav", ".m4a")):
            mode = "🎵 "
        elif path.endswith((".opus")):
            mode = "🎙 "
        elif path.endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
            mode = "🎞 "
        elif path.endswith((".zip", ".tar", ".tar.gz", ".rar", ".7z", ".xz")):
            mode = "🗜 "
        elif path.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico", ".webp")):
            mode = "🖼 "
        elif path.endswith((".exe", ".deb")):
            mode = "⚙️ "
        elif path.endswith((".iso", ".img")):
            mode = "💿 "
        elif path.endswith((".apk", ".xapk")):
            mode = "📱 "
        elif path.endswith((".py")):
            mode = "🐍 "
        else:
            mode = "📄 "
        time.ctime(os.path.getctime(path))
        time2 = time.ctime(os.path.getmtime(path))
        time3 = time.ctime(os.path.getatime(path))
        msg += f"<b>Lokasi :</b> <code>{path}</code>\n"
        msg += f"<b>Ikon :</b> <code>{mode}</code>\n"
        msg += f"<b>Ukuran :</b> <code>{yins.humanbytes(size)}</code>\n"
        msg += f"<b>Waktu Modifikasi Terakhir :</b> <code>{time2}</code>\n"
        msg += f"<b>Waktu Terakhir Diakses :</code> <code>{time3}</code>"

    if len(msg) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "ls.txt"
            await message.client.send_document(
                message.chat.id,
                out_file,
                caption=path,
            )
            os.remove(out_file.name)
    else:
        await message.reply(msg)
