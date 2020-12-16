""" Userbot module for other small commands. """
import sys
from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.z$")
async def shalom(e):
    await e.edit(f"[`Github Profile](https://github.com/rizgustiadi)`")
    CMD_HELP.update(
        {
            "z": "z.\
\nUsage: gives a nice Gitub Page as output."
        }
    )
