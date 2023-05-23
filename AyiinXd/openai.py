from random import choice

from pyAyiin import Ayiin, API_AI, CMD_HELP

from . import *


@Ayiin(["openai", "ai"])
async def open_ai(_, message):
    if len(message.command) == 1:
        return await message.reply(f"Ketik <code>{choice(hndlr)}ai [question]</code> Pertanyaan untuk menggunakan OpenAI")
    question = yins.get_cmd(message)
    msg = await message.reply("<code>Processing...</code>")
    try:
        date = await yins.post(
            "https://api.openai.com/v1/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_AI}",
            }, 
            json={
                "model": "text-davinci-003",
                "prompt": question,
                "max_tokens": 500,
                "temperature": 0,
            },
        )
        await msg.edit(date["choices"][0]["text"])
    except Exception:
        pass
    except BaseException as ex:
        await message.reply(f"ERROR: {ex}")


CMD_HELP.update(
    {"openai": (
        "openai",
        {
            "ai": "Berikan pertanyaan anda dan AI akan menjawabnya",
        }
        )
    }
)