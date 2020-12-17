""" Userbot module for other small commands. """
import sys
from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.akeno$")
async def shalom(e):
    await e.edit(f"Klik [`ini](https://github.com/rizgustiadi/AkenoXNew)`AkenoXNew Github Page")
    await e.(f"[`Github Profile](https://github.com/rizgustiadi)`")
    CMD_HELP.update(
        {
            "Akeno": ".akeno\
\nUsage: gives a nice Gitub Page as output."
        }
    )
