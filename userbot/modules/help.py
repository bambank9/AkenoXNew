# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot help command """

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.help(?: |$)(.*)")
async def help(event):
    """ For .help command,"""
    args = event.pattern_match.group(1).lower()
    # Prevent Channel Bug to get any information and commad from all modules
    if event.is_channel and not event.is_group:
        await event.edit("`Help Commad isn't permitted on channels`")
        return
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit("Yang Bener Tulis Modulnya.")
    else:
        string1 = "Harap tentukan modul mana yang Anda ingin bantuannya !!\nUsage: .help <nama modul>\n\n"
        string = "[ "
        string3 = "Daftar untuk semua perintah yang tersedia di bawah ini: "
        string2 = "-------------------------------------------------------------"
        for i in CMD_HELP:
            string += "`" + str(i)
            string += "`  ][  "
        await event.edit(
            f"{string1}" f"{string3}" f"{string2}\n" f"{string}" f"{string2}"
        )
        await asyncio.sleep(120)
        await event.delete()
