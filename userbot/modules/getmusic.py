# AnggaR96s

from telethon import events
import subprocess
from telethon.errors.rpcerrorlist import YouBlockedUserError
import asyncio
from userbot.events import register
from userbot import bot, CMD_HELP
import glob
import os

os.system("rm -rf *.mp3")


def bruh(name):
    os.system("instantmusic -q -s " + name)


@register(outgoing=True, pattern=r"^.song (.*)")
async def _(event):
    if event.fwd_from:
        return
    cmd = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    await event.edit("`Ok finding the song..`")
    bruh(str(cmd))
    l = glob.glob("*.mp3")
    loa = l[0]
    await event.edit("`Sending song..`")
    await event.client.send_file(
        event.chat_id,
        loa,
        force_document=True,
        allow_cache=False,
        caption=cmd,
        reply_to=reply_to_id,
    )
    os.system("rm -rf *.mp3")
    subprocess.check_output("rm -rf *.mp3", shell=True)
    await event.delete()


@register(outgoing=True, pattern="^.smd(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    link = event.pattern_match.group(1)
    chat = "@SpotifyMusicDownloaderBot"
    await event.edit("```Getting Your Music```")
    async with bot.conversation(chat) as conv:
        await asyncio.sleep(2)
        await event.edit("`Downloading music taking some times,  Stay Tuned.....`")
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=752979930)
            )
            await bot.send_message(chat, link)
            respond = await response
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.reply(
                "```Please unblock @SpotifyMusicDownloaderBot and try again```"
            )
            return
        await event.delete()
        await bot.forward_messages(event.chat_id, respond.message)
        await bot.send_read_acknowledge(event.chat_id)

@register(outgoing=True, pattern="^.nts (?: |$)(.*)")
async def WooMai(netase):
    if netase.fwd_from:
        return
    song = netase.pattren_match.group(1)
    chat = "@WooMaiBot"
    link = f"/netease {song}"
    await netase.edit("```Getting Your Music```")    
    async with bot.conversation(chat) as conv:
        await asyncio.sleep(2)
        await netase.edit("`Downloading.... Please Wait`")
        try:
            msg = await conv.send_message(link)
            response = await conv.get_response()
            respond = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await netase.reply("```Please unblock @WooMaiBot and try again```")
            return
        await netase.edit("`Sending Your Music`")
        await asyncio.sleep(3)
        await bot.send_file(netase.chat_id, respond)
    msg = await netase.client.delete_messages(
        conv.chat_id [msg.id, response.id, respond.id]
    )
    await msg.edit(
        f"Song name - __{link}__\nUploaded by [AkenoXNew]"
    )
    await netase.delete()
        

CMD_HELP.update(
    {
        "song": ">`.song` **atrist title**"
        "\nUsage: Finding and uploading song.\n"
        ">`.nts` **<Song Title>**"
        "\nUsage: **Download music with @WooMaiBot**\n"
        ">`.smd` **<song tittle>**"
        "\nUsage: **Download music from spotify**"
    }
)
