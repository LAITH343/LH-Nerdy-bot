import os
from aiogram import Bot

# importing env var from .env or system
# if u don't wont to use env var u can add them like bot_owner = 0000000000 and so on for the others
try:
    from dotenv import load_dotenv

    # load .env file
    load_dotenv()
    # import bot token from .env file
    bot_token = os.getenv('BOT_TOKEN')
    bot_owner = os.getenv('BOT_OWNER')
    log_chat_id = os.getenv('LOG_CHAT_ID')
    errors_chat_id = os.getenv('ERRORS_CHAT_ID')
except:
    bot_token = os.environ.get('BOT_TOKEN')
    bot_owner = os.environ.get('BOT_OWNER')
    log_chat_id = os.environ.get('LOG_CHAT_ID')
    errors_chat_id = os.environ.get('ERRORS_CHAT_ID')

bot = Bot(token=bot_token)

