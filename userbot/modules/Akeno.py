""" Userbot module for other small commands. """
import sys
from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.akeno$")
async def shalom(e):
    await e.edit(
        f"    🌪 My Repo 🌪\n"
        f" ➥ [AkenoXNew](https://github.com/rizgustiadi/AkenoXNew)\n")
    CMD_HELP.update(
        {
            "Akeno": ".akeno\
\nUsage: gives a nice Gitub Page as output."
        }
    )
