import asyncio
from aiogram import types

async def report(message, bot, func, error):
    await bot.send_message(-708189144, f"error occurred with @{message.from_user.username}\nat function {func}\n{error}")

