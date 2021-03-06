# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
"""Userbot module containing various scrapers."""
 
import os
import time
import asyncio
import shutil
import json
from bs4 import BeautifulSoup
import re
from re import findall
from urllib.parse import quote_plus
from urllib.error import HTTPError
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError
from urbandict import define
from requests import get
from search_engine_parser import GoogleSearch
from google_trans_new import LANGUAGES, google_translator
from gtts import gTTS
from gtts.lang import tts_langs
from emoji import get_emoji_regexp
from youtube_search import YoutubeSearch
from youtube_dl import YoutubeDL
from youtube_dl.utils import (DownloadError, ContentTooShortError,
                              ExtractorError, GeoRestrictedError,
                              MaxDownloadsReached, PostProcessingError,
                              UnavailableVideoError, XAttrMetadataError)
from asyncio import sleep
from userbot import (CMD_HELP, BOTLOG, BOTLOG_CHATID,
                     TEMP_DOWNLOAD_DIRECTORY)
from userbot.events import register
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
from userbot.utils import progress, chrome, googleimagesdownload
 
from userbot.modules.upload_download import get_video_thumb


CARBONLANG = "auto"
TTS_LANG = "id"
TRT_LANG = "en"
 
 
@register(outgoing=True, pattern="^.crblang (.*)")
async def setlang(prog):
    global CARBONLANG
    CARBONLANG = prog.pattern_match.group(1)
    await prog.edit(f"Language for carbon.now.sh set to {CARBONLANG}")
 
 
@register(outgoing=True, pattern="^.carbon")
async def carbon_api(e):
    """A Wrapper for carbon.now.sh"""
    await e.edit("`Processing...`")
    CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'
    global CARBONLANG
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[8:]:
        pcode = str(pcode[8:])
    elif textx:
        pcode = str(textx.message)  # Importing message to module
    code = quote_plus(pcode)  # Converting to urlencoded
    await e.edit("`Processing...\n25%`")
    file_path = TEMP_DOWNLOAD_DIRECTORY + "carbon.png"
    if os.path.isfile(file_path):
        os.remove(file_path)
    url = CARBON.format(code=code, lang=CARBONLANG)
    driver = await chrome()
    driver.get(url)
    await e.edit("`Processing...\n50%`")
    driver.find_element_by_xpath("//button[@id='export-menu']").click()
    driver.find_element_by_xpath("//button[contains(text(),'4x')]").click()
    driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
    await e.edit("`Processing...\n75%`")
    # Waiting for downloading
    while not os.path.isfile(file_path):
        await sleep(0.5)
    await e.edit("`Processing...\n100%`")
    await e.edit("`Uploading...`")
    await e.client.send_file(
        e.chat_id,
        file_path,
        caption=("Made using [Carbon](https://carbon.now.sh/about/),"
                 "\na project by [Dawn Labs](https://dawnlabs.io/)"),
        force_document=True,
        reply_to=e.message.reply_to_msg_id,
    )
 
    os.remove(file_path)
    driver.quit()
    # Removing carbon.png after uploading
    await e.delete()  # Deleting msg
 
 

 
@register(outgoing=True, pattern=r"^\.currency ([\d\.]+) ([a-zA-Z]+) ([a-zA-Z]+)")
async def moni(event):
    c_from_val = float(event.pattern_match.group(1))
    c_from = (event.pattern_match.group(2)).upper()
    c_to = (event.pattern_match.group(3)).upper()
    try:
        response = get(
            "https://api.ratesapi.io/api/latest",
            params={"base": c_from, "symbols": c_to},
        ).json()
    except Exception:
        await event.edit("**Error: API is down.**")
        return
    if "error" in response:
        await event.edit(
            "**This seems to be some alien currency, which I can't convert right now.**"
        )
        return
    c_to_val = round(c_from_val * response["rates"][c_to], 2)
    await event.edit(f"**{c_from_val} {c_from} = {c_to_val} {c_to}**")
 
 
@register(outgoing=True, pattern=r"^.google (.*)")
async def gsearch(q_event):
    """For .google command, do a Google search."""
    match = q_event.pattern_match.group(1)
    page = findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(match), int(page))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    msg = ""
    for i in range(7):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"[{title}]({link})\n`{desc}`\n\n"
        except IndexError:
            break
    await q_event.edit("**Search Query:**\n`" + match + "`\n\n**Results:**\n" +
                       msg,
                       link_preview=False)
 
    if BOTLOG:
        await q_event.client.send_message(
            BOTLOG_CHATID,
            "Google Search query `" + match + "` was executed successfully",
        )
 
 
@register(outgoing=True, pattern=r"^.wiki (.*)")
async def wiki(wiki_q):
    """For .wiki command, fetch content from Wikipedia."""
    match = wiki_q.pattern_match.group(1)
    try:
        summary(match)
    except DisambiguationError as error:
        return await wiki_q.edit(f"Disambiguated page found.\n\n{error}")
    except PageError as pageerror:
        return await wiki_q.edit(f"Page not found.\n\n{pageerror}")
    result = summary(match)
    if len(result) >= 4096:
        file = open("output.txt", "w+")
        file.write(result)
        file.close()
        await wiki_q.client.send_file(
            wiki_q.chat_id,
            "output.txt",
            reply_to=wiki_q.id,
            caption="`Output too large, sending as file`",
        )
        if os.path.exists("output.txt"):
            return os.remove("output.txt")
    await wiki_q.edit("**Search:**\n`" + match + "`\n\n**Result:**\n" + result)
    if BOTLOG:
        await wiki_q.client.send_message(
            BOTLOG_CHATID, f"Wiki query `{match}` was executed successfully")
 
 
@register(outgoing=True, pattern="^.ud (.*)")
async def urban_dict(ud_e):
    """For .ud command, fetch content from Urban Dictionary."""
    await ud_e.edit("Processing...")
    query = ud_e.pattern_match.group(1)
    try:
        define(query)
    except HTTPError:
        return await ud_e.edit(f"Sorry, couldn't find any results for: {query}")
    mean = define(query)
    deflen = sum(len(i) for i in mean[0]["def"])
    exalen = sum(len(i) for i in mean[0]["example"])
    meanlen = deflen + exalen
    if int(meanlen) >= 0:
        if int(meanlen) >= 4096:
            await ud_e.edit("`Output too large, sending as file.`")
            file = open("output.txt", "w+")
            file.write("Text: " + query + "\n\nMeaning: " + mean[0]["def"] +
                       "\n\n" + "Example: \n" + mean[0]["example"])
            file.close()
            await ud_e.client.send_file(
                ud_e.chat_id,
                "output.txt",
                caption="`Output was too large, sent it as a file.`")
            if os.path.exists("output.txt"):
                os.remove("output.txt")
            return await ud_e.delete()
        await ud_e.edit("Text: **" + query + "**\n\nMeaning: **" +
                        mean[0]["def"] + "**\n\n" + "Example: \n__" +
                        mean[0]["example"] + "__")
        if BOTLOG:
            await ud_e.client.send_message(
                BOTLOG_CHATID,
                "ud query `" + query + "` executed successfully.")
    else:
        await ud_e.edit("No result found for **" + query + "**")
 
 
@register(outgoing=True, pattern=r"^.tts(?: |$)([\s\S]*)")
async def text_to_speech(query):
    """For .tts command, a wrapper for Google Text-to-Speech."""
    textx = await query.get_reply_message()
    message = query.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await query.edit(
            "`Give a text or reply to a message for Text-to-Speech!`")
 
    try:
        gTTS(message, lang=TTS_LANG)
    except AssertionError:
        return await query.edit(
            'The text is empty.\n'
            'Nothing left to speak after pre-precessing, tokenizing and cleaning.'
        )
    except ValueError:
        return await query.edit('Language is not supported.')
    except RuntimeError:
        return await query.edit('Error loading the languages dictionary.')
    tts = gTTS(message, lang=TTS_LANG)
    tts.save("k.mp3")
    with open("k.mp3", "rb") as audio:
        linelist = list(audio)
        linecount = len(linelist)
    if linecount == 1:
        tts = gTTS(message, lang=TTS_LANG)
        tts.save("k.mp3")
    with open("k.mp3", "r"):
        await query.client.send_file(query.chat_id, "k.mp3", voice_note=True)
        os.remove("k.mp3")
        if BOTLOG:
            await query.client.send_message(
                BOTLOG_CHATID, "Text to Speech executed successfully !")
        await query.delete()
 
 
# kanged from Blank-x ;---;
@register(outgoing=True, pattern="^.imdb (.*)")
async def imdb(e):
    try:
        movie_name = e.pattern_match.group(1)
        remove_space = movie_name.split(' ')
        final_name = '+'.join(remove_space)
        page = get("https://www.imdb.com/find?ref_=nv_sr_fn&q=" + final_name +
                   "&s=all")
        soup = BeautifulSoup(page.content, 'lxml')
        odds = soup.findAll("tr", "odd")
        mov_title = odds[0].findNext('td').findNext('td').text
        mov_link = "http://www.imdb.com/" + \
            odds[0].findNext('td').findNext('td').a['href']
        page1 = get(mov_link)
        soup = BeautifulSoup(page1.content, 'lxml')
        if soup.find('div', 'poster'):
            poster = soup.find('div', 'poster').img['src']
        else:
            poster = ''
        if soup.find('div', 'title_wrapper'):
            pg = soup.find('div', 'title_wrapper').findNext('div').text
            mov_details = re.sub(r'\s+', ' ', pg)
        else:
            mov_details = ''
        credits = soup.findAll('div', 'credit_summary_item')
        director = credits[0].a.text
        if len(credits) == 1:
            writer = 'Not available'
            stars = 'Not available'
        elif len(credits) > 2:
            writer = credits[1].a.text
            actors = []
            for x in credits[2].findAll('a'):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + ',' + actors[1] + ',' + actors[2]
        else:
            writer = 'Not available'
            actors = []
            for x in credits[1].findAll('a'):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + ',' + actors[1] + ',' + actors[2]
        if soup.find('div', "inline canwrap"):
            story_line = soup.find('div',
                                   "inline canwrap").findAll('p')[0].text
        else:
            story_line = 'Not available'
        info = soup.findAll('div', "txt-block")
        if info:
            mov_country = []
            mov_language = []
            for node in info:
                a = node.findAll('a')
                for i in a:
                    if "country_of_origin" in i['href']:
                        mov_country.append(i.text)
                    elif "primary_language" in i['href']:
                        mov_language.append(i.text)
        if soup.findAll('div', "ratingValue"):
            for r in soup.findAll('div', "ratingValue"):
                mov_rating = r.strong['title']
        else:
            mov_rating = 'Not available'
        await e.edit('<a href=' + poster + '>???</a>'
                     '<b>Title : </b><code>' + mov_title + '</code>\n<code>' +
                     mov_details + '</code>\n<b>Rating : </b><code>' +
                     mov_rating + '</code>\n<b>Country : </b><code>' +
                     mov_country[0] + '</code>\n<b>Language : </b><code>' +
                     mov_language[0] + '</code>\n<b>Director : </b><code>' +
                     director + '</code>\n<b>Writer : </b><code>' + writer +
                     '</code>\n<b>Stars : </b><code>' + stars +
                     '</code>\n<b>IMDB Url : </b>' + mov_link +
                     '\n<b>Story Line : </b>' + story_line,
                     link_preview=True,
                     parse_mode='HTML')
    except IndexError:
        await e.edit("Plox enter **Valid movie name** kthx")


@register(outgoing=True, pattern=r"^\.trt(?: |$)([\s\S]*)")
async def translateme(trans):
    """ For .trt command, translate the given text using Google Translate. """

    if trans.is_reply and not trans.pattern_match.group(1):
        message = await trans.get_reply_message()
        message = str(message.message)
    else:
        message = str(trans.pattern_match.group(1))

    if not message:
        return await trans.edit(
            "**Give some text or reply to a message to translate!**")

    await trans.edit("**Processing...**")
    translator = google_translator()
    try:
        reply_text = translator.translate(deEmojify(message),
                                          lang_tgt=TRT_LANG)
    except ValueError:

        return await trans.edit(
            "**Invalid language selected, use **`.lang tts <language code>`**.**"
        )

    try:
        source_lan = translator.detect(deEmojify(message))[1].title()
    except:
        source_lan = "(Google didn't provide this info)"

    reply_text = f"From: **{source_lan}**\nTo: **{LANGUAGES.get(TRT_LANG).title()}**\n\n{reply_text}"

    await trans.edit(reply_text)


@register(pattern=".lang (trt|tts) (.*)", outgoing=True)
async def lang(value):
    """For .lang command, change the default langauge of userbot scrapers."""
    util = value.pattern_match.group(1).lower()
    if util == "trt":
        scraper = "Translator"
        global TRT_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in LANGUAGES:
            TRT_LANG = arg
            LANG = LANGUAGES[arg]
        else:
            return await value.edit(
                f"`Invalid Language code !!`\n`Available language codes for TRT`:\n\n`{LANGUAGES}`"
            )
    elif util == "tts":
        scraper = "Text to Speech"
        global TTS_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in tts_langs():
            TTS_LANG = arg
            LANG = tts_langs()[arg]
        else:
            return await value.edit(
                f"`Invalid Language code !!`\n`Available language codes for TTS`:\n\n`{tts_langs()}`"
            )
    await value.edit(f"`Language for {scraper} changed to {LANG.title()}.`")
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID,
            f"`Language for {scraper} changed to {LANG.title()}.`")
 
 
@register(outgoing=True, pattern="^.yt (.*)")
async def yt_search(video_q):
    """For .yt command, do a YouTube search from Telegram."""
    query = video_q.pattern_match.group(1)
    if not query:
        await video_q.edit("`Enter query to search`")
    await video_q.edit("`Processing...`")
    try:
        results = json.loads(YoutubeSearch(query, max_results=7).to_json())
    except KeyError:
        return await video_q.edit("`Youtube Search gone retard.\nCan't search this query!`")
    output = f"**Search Query:**\n`{query}`\n\n**Results:**\n\n"
    for i in results["videos"]:
        output += (f"??? `{i['title']}`\nhttps://www.youtube.com{i['url_suffix']}\n\n")
    await video_q.edit(output, link_preview=False)
 
 
@register(outgoing=True, pattern=r".rip(audio|video) (.*)")
async def download_video(v_url):
    """For .rip command, download media from YouTube and many other sites."""
    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()
 
    await v_url.edit("`Preparing to download...`")
 
    if type == "audio":
        opts = {
            'format':
            'bestaudio',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'writethumbnail':
            True,
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl':
            '%(id)s.mp3',
            'quiet':
            True,
            'logtostderr':
            False
        }
        video = False
        song = True
 
    elif type == "video":
        opts = {
            'format':
            'best',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'outtmpl':
            '%(id)s.mp4',
            'logtostderr':
            False,
            'quiet':
            True
        }
        song = False
        video = True
 
    try:
        await v_url.edit("`Fetching data, please wait..`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        return await v_url.edit(f"`{str(DE)}`")
    except ContentTooShortError:
        return await v_url.edit("`The download content was too short.`")
    except GeoRestrictedError:
        return await v_url.edit(
            "`Video is not available from your geographic location "
            "due to geographic restrictions imposed by a website.`"
        )
    except MaxDownloadsReached:
        return await v_url.edit("`Max-downloads limit has been reached.`")
    except PostProcessingError:
        return await v_url.edit("`There was an error during post processing.`")
    except UnavailableVideoError:
        return await v_url.edit("`Media is not available in the requested format.`")
    except XAttrMetadataError as XAME:
        return await v_url.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        return await v_url.edit("`There was an error during info extraction.`")
    except Exception as e:
        return await v_url.edit(f"{str(type(e)): {str(e)}}")
    c_time = time.time()
    if song:
        await v_url.edit(f"**Preparing to upload song:**\n**{rip_data['title']}**")
        with open(rip_data["id"] + ".mp3", "rb") as f:
            result = await upload_file(
                client=v_url.client,
                file=f,
                name=f"{rip_data['id']}.mp3",
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d,
                        t,
                        v_url,
                        c_time,
                        "YouTube-DL - Upload",
                        f"{rip_data['title']}.mp3",
                    )
                ),
            )
        img_extensions = ["jpg", "jpeg", "webp"]
        img_filenames = [
            fn_img
            for fn_img in os.listdir()
            if any(fn_img.endswith(ext_img) for ext_img in img_extensions)
        ]
        thumb_image = img_filenames[0]
        await v_url.client.send_file(
            v_url.chat_id,
            result,
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(rip_data["duration"]),
                    title=str(rip_data["title"]),
                    performer=str(rip_data["uploader"]),
                )
            ],
            thumb=thumb_image,
        )
        os.remove(thumb_image)
        os.remove(f"{rip_data['id']}.mp3")
        await v_url.delete()
    elif video:
        await v_url.edit(f"**Preparing to upload video:**\n**{rip_data['title']}**")
        thumb_image = await get_video_thumb(rip_data["id"] + ".mp4", "thumb.png")
        with open(rip_data["id"] + ".mp4", "rb") as f:
            result = await upload_file(
                client=v_url.client,
                file=f,
                name=f"{rip_data['id']}.mp4",
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d,
                        t,
                        v_url,
                        c_time,
                        "YouTube-DL - Upload",
                        f"{rip_data['title']}.mp4",
                    )
                ),
            )
        await v_url.client.send_file(
            v_url.chat_id,
            result,
            thumb=thumb_image,
            attributes=[
                DocumentAttributeVideo(
                    duration=rip_data["duration"],
                    w=rip_data["width"],
                    h=rip_data["height"],
                    supports_streaming=True,
                )
            ],
            caption=rip_data["title"],
        )
        os.remove(f"{rip_data['id']}.mp4")
        os.remove(thumb_image)
        await v_url.delete()
  
 
def deEmojify(inputString):
    """Remove emojis and other non-safe characters from string"""
    return get_emoji_regexp().sub(u'', inputString)
 
 
def deEmojify(inputString):
    """Remove emojis and other non-safe characters from string"""
    return get_emoji_regexp().sub(u'', inputString)
 
 
CMD_HELP.update({
    'currency':
    '`.currency` <amount> <from> <to>\
        \nUsage: Converts various currencies for you.'
})
CMD_HELP.update({
    'carbon':
    '`.carbon` <text> [or reply]\
        \nUsage: Beautify your code using carbon.now.sh\nUse .crblang <text> to set language for your code.'
})
CMD_HELP.update(
    {'google': '`.google` <query>\
        \nUsage: Does a search on Google.'})
CMD_HELP.update(
    {'wiki': '`.wiki` <query>\
        \nUsage: Does a search on Wikipedia.'})
CMD_HELP.update(
    {'ud': '`.ud` <query>\
        \nUsage: Does a search on Urban Dictionary.'})
CMD_HELP.update({
    'tts':
    '`.tts` <text> [or reply]\
        \nUsage: Translates text to speech for the language which is set.\nUse .lang tts <language code> to set language for tts. (Default is English.)'
})
CMD_HELP.update({
    'trt':
    '`.trt` <text> [or reply]\
        \nUsage: Translates text to the language which is set.\nUse .lang trt <language code> to set language for trt. (Default is English)'
})
CMD_HELP.update({'yt': '`.yt` <text>\
        \nUsage: Does a YouTube search.'})
CMD_HELP.update(
    {"imdb": "`.imdb` <movie-name>\nShows movie info and other stuff."})
CMD_HELP.update({
    'rip':
    '`.ripaudio` <url> or ripvideo <url>\
        \nUsage: Download videos and songs from YouTube (and [many other sites](https://ytdl-org.github.io/youtube-dl/supportedsites.html)).'
})
 
