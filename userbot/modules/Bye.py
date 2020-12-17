""" Userbot module for other small commands. """
import sys
from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.bye$")
async def shalom(e):
    await e.edit(f"[{user.first_name}](tg://user?id={user.id}) Hast Left The Chat")
    CMD_HELP.update(
        {
            "Bye": ".bye\
\nUsage: gives a nice Gitub Page as output."
        }
    )
