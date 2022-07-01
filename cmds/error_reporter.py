from config import errors_chat_id

async def report(message, bot, func, error):
    await bot.send_message(int(errors_chat_id), f"""
error occurred with @{message.from_user.username}
at function {func}
{error}
user ID: {message.from_user.id}
""")

