from cmds import user_manager, error_reporter
from cmds.books_manager import get_extra_files_list, get_extra_file_by_name, get_file_by_name, get_files_list
from cmds.classes import GetFile, GetBook
from cmds.markup_manager import get_user_markup
from config import bot


async def upload_file(message, state):
    try:
        await message.answer("جاري رفع الملف", reply_markup=get_user_markup(message.from_user.id))
        await bot.send_document(message.chat.id, document=open(
            get_extra_file_by_name(user_manager.check_user_stage(message.from_user.id), message.text), 'rb'))
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "main - upload extra handler", e)


async def upload_book(message, state):
    try:
        await message.answer("جاري رفع الكتاب", reply_markup=get_user_markup(message.from_user.id))
        await bot.send_document(message.chat.id, document=open(
            get_file_by_name(user_manager.check_user_stage(message.from_user.id), message.text), 'rb'))
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "main - upload book handler", e)


def reg(dp):
    dp.register_message_handler(upload_file, lambda message: message.text in get_extra_files_list(user_manager.check_user_stage(message.from_user.id)), state=GetFile.temp)
    dp.register_message_handler(upload_book, lambda message: message.text in get_files_list(user_manager.check_user_stage(message.from_user.id)), state=GetBook.temp)
