# Adapted from OpenUserBot for Uniborg

"""Download & Upload Images on Telegram\n
Syntax: `.img <Name>` or `.img (replied message)`
\n Upgraded and Google Image Error Fixed by @NeoMatrix90 aka @kirito6969
"""

import os
import shutil
from re import findall


from userbot import CMD_HELP
from userbot.google_images_download import googleimagesdownload
from userbot.events import register

@register(outgoing=True, pattern=r"^.img (.*)")
async def img_sampler(event):
    await event.edit("`Processing ...`")
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        query = reply.message
    else:
        await event.edit("`What I am Supposed to Search u Dumb Ass(Donkey)`")
        return

    lim = findall(r"lim=\d+", query)
    # lim = event.pattern_match.group(1)
    try:
        lim = lim[0]
        lim = lim.replace("lim=", "")
        query = query.replace("lim=" + lim[0], "")
    except IndexError:
        lim = 5
    response = googleimagesdownload()

    # creating list of arguments
    arguments = {
        "keywords": query,
        "limit": lim,
        "format": "jpg",
        "no_directory": "no_directory",
    }

    # passing the arguments to the function
    paths = response.download(arguments)
    lst = paths[0][query]
    await event.client.send_file(
        await event.client.get_input_entity(event.chat_id), lst
    )
    shutil.rmtree(os.path.dirname(os.path.abspath(lst[0])))
    await event.delete()

CMD_HELP.update(
        {
            "img": ".img\
\nUsage: untuk mencari gambar"
        }
    )
