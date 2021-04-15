# For @UniBorg

# Courtesy @yasirsiddiqui

"""

.out

"""


import time

from telethon.tl.functions.channels import LeaveChannelRequest

from userbot import CMD_HELP,bot
from userbot.events import register

@register(outgoing=True, pattern="^out$")
async def shalom(e):
    x = await bot.get_me()
    name = x.first_name
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):

        await e.edit(f"[{x.first_name}](tg://user?id={user.id}) has left this group, bye!!")

        time.sleep(3)

        if "-" in str(e.chat_id):

            await borg(LeaveChannelRequest(e.chat_id))

        else:

            await e.edit("`This is Not A Chat. Please use this in groups :/`")


CMD_HELP.update({"out": ".out\nUse - Leave the group."})
