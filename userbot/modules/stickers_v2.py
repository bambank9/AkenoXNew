from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
import io
from userbot import bot, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.get$")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("Balas di Sticker Goblok!!")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("Balas di Sticker Tolol!!")
        return
    chat = "@stickers_to_image_bot"
    await event.edit("Convert to image..")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=611085086))
              response = await response
            if response.text.startswith("..."):
                response = conv.wait_event(
                    events.NewMessage(
                        incoming=True,
                        from_users=611085086))
                response = await response
                await event.delete()
                await event.client.send_message(event.chat_id, response.message, reply_to=reply_message.id)
                await event.client.delete_message(event.chat_id, [msg.id, response.id])
            else:
                await event.edit("try again")
        await bot.send_read_acknowledge(conv.chat_id)     
        
        
CMD_HELP.update(
    {
        "stickers_v2": ">`.itos`"
        "\nUsage: Reply .itos to a sticker or an image to kang it to your userbot no pack "
        "\n\n>`.get`"
        "\nUsage: reply to a sticker to get 'PNG' file of sticker."
        "\n\n>`.stoi`"
        "\nUsage: reply to a sticker to get 'PNG' file of sticker."})