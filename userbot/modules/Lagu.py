# zal

from telethon import events
import subprocess
from telethon.errors.rpcerrorlist import YouBlockedUserError
import asyncio
from userbot.events import register
from userbot import bot, CMD_HELP
import glob
import os

try:
    pass
except BaseException:
    os.system("pip install instantmusic")

os.system("rm -rf *.mp3")


def bruh(name):
    os.system("instantmusic -q -s " + name)


@register(outgoing=True, pattern="^.netease(?: |$)(.*)")
async def WooMai(event):
    if event.fwd_from:
        return
    song = event.pattren_match.group(1)
    chat = "@WooMaiBot"
    link = f"/netease {song}"
    await event.edit("```Getting Your Music```")    
    async with bot.conversation(chat) as conv:
        await asyncio.sleep(2)
        await event.edit("`Downloading.... Please Wait`")
        try:
            msg = await conv.send_message(link)
            response = await conv.get_response()
            respond = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.reply("```Please unblock @WooMaiBot and try again```")
            return
        await event.edit("`Sending Your Music`")
        await asyncio.sleep(3)
        await bot.send_file(event.chat_id, respond)
    msg = await event.client.delete_messages(
        conv.chat_id [msg.id, response.id, respond.id]
    )
    await msg.edit(
        f"Song name - __{link}__\nUploaded by [AkenoXNew]"
    )
    await event.delete()


CMD_HELP.update(
    {
        "Lagu": ".netease <Artist - Song Title>\
             \nUsage:Download music with @WooMaiBot."
    }
)
