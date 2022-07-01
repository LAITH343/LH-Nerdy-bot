from config import log_chat_id

async def send_log(message, bot, func, msg):
    await bot.send_message(int(log_chat_id), f"""
أستعمل  @{message.from_user.username} {func} 

{msg}
""")
