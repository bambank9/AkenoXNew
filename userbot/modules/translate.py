from google_trans_new import LANGUAGES, google_translator



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
