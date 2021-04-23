import asyncio
import os

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import CMD_HELP, bot
from userbot.events import register

@register(outgoing=True, pattern=r"^.nts (.*)")
async def WooMai(netase):
    if netase.fwd_from:
        return
    track = str(artist) + " - " + str(song)
    chat = "@WooMaiBot"
    link = f"/netease {track}"
    await event.edit("`Searching...`")
    try:
        async with bot.conversation(chat) as conv:
            await asyncio.sleep(2)
            await event.edit("`Processing... Please wait`")
            try:
                msg = await conv.send_message(link)
                response = await conv.get_response()
                respond = await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.reply("`Please unblock @WooMaiBot and try again`")
                return
            await event.edit("`Sending Your Music...`")
            await asyncio.sleep(3)
            await bot.send_file(event.chat_id, respond)
        await event.client.delete_messages(
            conv.chat_id, [msg.id, response.id, respond.id]
        )
        await event.delete()
    except TimeoutError:
        return await event.edit(
            "`Error: `@WooMaiBot` is not responding or Song not found!.`"
        )

CMD_HELP.update(
        {
            "womai": ".nts\
\nUsage: gives a nice Gitub Page as output."
        }
    )
