async def send_log(message, bot, func, msg):
    await bot.send_message(-746881108, f"""
أستعمل  @{message.from_user.username} {func} 

{msg}
""")
