import logging
from aiogram import Dispatcher, executor, types
from cmds import user_manager, error_reporter
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from cmds.markup_manager import get_user_markup
from cmds.user_manager import check_user_not_req, check_user_exist, update_user_info, check_username_changed, \
    get_user_username
from commands_handlers import tools_handler, main_menu_handler, admin_menu_handler, manager_menu_handler, view_hw_handler, unkown_message_handler, upload_files_handler
from config import bot, bot_owner

# Configure logging
logging.basicConfig(level=logging.INFO)
# create memory storage for dipatcher
storage = MemoryStorage()

# Initialize bot and dispatcher
dp = Dispatcher(bot, storage=storage)


# create add admin handler
@dp.message_handler(commands=['addadmin'])
async def add_admin(message: types.Message, state: FSMContext):
    if message.from_user.id == int(bot_owner):
        user_manager.add_admin(message.get_full_command()[1])
        await message.answer("تم الاضافة")
    else:
        await message.answer("ليس لديك الصلاحيات ﻷجراء هذا الامر")


# create remove admin handler
@dp.message_handler(commands=["deladmin"])
async def add_admin(message: types.Message, state: FSMContext):
    if message.from_user.id == int(bot_owner):
        user_manager.del_admin(message.get_full_command()[1])
        await message.answer("تم الحذف")
    else:
        await message.answer("ليس لديك الصلاحيات ﻷجراء هذا الامر")


# check if the user already added into the system
@dp.message_handler(lambda message: not check_user_exist(message.from_user.id))
async def Not_inside_sys(message: types.Message):
    await message.answer(f"أنت غير مسجل اطلب من ممثل المرحلة أضافتك\n الID الخاص بك {message.from_user.id}", reply_markup=types.ReplyKeyboardRemove())


# check user not register
@dp.message_handler(lambda message: check_user_not_req(message.from_user.id) == True)
async def Get_user_info(message: types.Message):
    try:
        update_user_info(message.from_user.id, message.from_user.full_name, message.from_user.username)
        await message.answer("أهلا بك في البوت", reply_markup=get_user_markup(message.from_user.id))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "main - check user not req", e)


# check user username if it was changed
@dp.message_handler(lambda message: check_username_changed(message.from_user.id, message.from_user.username) == True)
async def username_changed(message: types.Message):
    await message.answer(f"لقد قمت بتغيير أسم المستخدم (اليوزر) الخاص بك\n يرجى الرجوع الى {get_user_username(message.from_user.id)} أو أطلب من المسؤول حذفك و أضافتك من جديد", reply_markup=types.ReplyKeyboardRemove())


# create start message/command handler
@dp.message_handler(lambda message: message.text in ["start", "بدء", "/start"])
async def start_message(message: types.Message):
    try:
        await bot.send_message(message.chat.id, "أهلا بك في البوت", reply_markup=get_user_markup(message.from_user.id))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "main - start message/command handler", e)


if __name__ == '__main__':
    upload_files_handler.reg(dp)
    main_menu_handler.reg(dp)
    admin_menu_handler.reg(dp)
    manager_menu_handler.reg(dp)
    tools_handler.reg(dp)
    view_hw_handler.reg(dp)
    unkown_message_handler.reg(dp)
    executor.start_polling(dp, skip_updates=True)
