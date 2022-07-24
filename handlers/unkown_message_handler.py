async def unknow_messages(message):
    await message.reply("""
عذرا لم افهم ماذا تقول
يمكنك ارسال بدء لعرض الاوامر أو اضغط على
/start
""")


def reg(dp):
    dp.register_message_handler(unknow_messages)