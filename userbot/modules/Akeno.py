""" Userbot module for other small commands. """
import sys
from userbot import CMD_HELP,USERS,bot
from userbot.events import register


@register(outgoing=True, pattern="^.akeno$")
async def shalom(e):
    global USERS
    x = await bot.get_me()
    x.username = x.first_name
    await e.edit(
        f"    🌪 My Repo 🌪\n\n"
        f" ➥ [AkenoXNew](https://github.com/rizgustiadi/AkenoXNew)\n\n"
        f" ┈┈┈╭━━━━━╮┈┈┈┈┈\n"
        f" ┈┈┈┃┊┊┊┊┊┃┈┈┈┈┈\n"
        f" ┈┈┈┃┊┊╭━╮┻╮┈┈┈┈\n"
        f" ┈┈┈╱╲┊┃▋┃▋┃┈┈┈┈\n"
        f" ┈┈╭┻┊┊╰━┻━╮┈┈┈┈\n"
        f" ┈┈╰┳┊╭━━━┳╯┈┈┈┈\n"
        f" ┈┈┈┃┊┃╰━━┫┈Owner [{x.first_name}](tg://user?id={user.id})\n" 
        f" ┈┈┈┈┈┈┏━┓┈┈┈┈┈┈")
    CMD_HELP.update(
        {
            "Akeno": ".akeno\
\nUsage: gives a nice Gitub Page as output."
        }
    )
