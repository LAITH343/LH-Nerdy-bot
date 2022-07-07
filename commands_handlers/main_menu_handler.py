from aiogram import types
from cmds import error_reporter, user_manager
from cmds.markup_manager import manager_markup, admin_markup, get_user_markup, custom_markup, books_markup, extra_file_markup
from cmds.myinfo import myInfo
from cmds.user_manager import check_admin, check_user_exist, get_manager_stage, check_user_stage
from cmds.classes import GetBook, GetFile
from cmds.books_manager import get_files_list, get_extra_files_list
from config import bot


async def View_manager_list(message):
    if get_manager_stage(message.from_user.id):
        await message.reply("تم عرض صلاحيات المشرف", reply_markup=manager_markup())
    else:
        await message.reply("ليس لديك الصلاحية لعرض هذه القائمة", reply_markup=get_user_markup(message.from_user.id))


async def View_admin_list(message):
    if check_admin(message.from_user.id):
        await message.reply("تم عرض صلاحيات الادمن", reply_markup=admin_markup())
    else:
        await message.reply("ليس لديك الصلاحية لعرض هذه القائمة", reply_markup=get_user_markup(message.from_user.id))


async def View_hw_menu(message):
    if not check_user_exist(message.from_user.id):
        await bot.send_message(message.chat.id, "أنت غير مسجل اطلب من ممثل المرحلة أضافتك", reply_markup=get_user_markup(message.from_user.id))
    else:
        await bot.send_message(message.chat.id, "اختر اليوم من القائمة", reply_markup=custom_markup(["اختيار يوم 📋","عرض واجبات الاسبوع 📖","الرجوع للقائمة الرئيسية 🏠"]))


async def tools_menu(message):
    if not check_user_exist(message.from_user.id):
        await bot.send_message(message.chat.id, "أنت غير مسجل اطلب من ممثل المرحلة أضافتك")
    else:
        await message.reply("أختر من القائمة", reply_markup=custom_markup(["دمج ملفات pdf","تحويل الصور الى pdf","الرجوع للقائمة الرئيسية 🏠"]))


async def Books_View(message):
    if not check_user_exist(message.from_user.id):
        message.answer("أنت غير مسجل اطلب من ممثل المرحلة أضافتك", reply_markup=get_user_markup(message.from_user.id))
    else:
        if get_files_list(check_user_stage(message.from_user.id)):
            await GetBook.temp.set()
        await message.answer("اختر كاتب من القائمة", reply_markup=books_markup(get_files_list(check_user_stage(message.from_user.id))))


async def Extra_file_View(message):
    if not check_user_exist(message.from_user.id):
        message.answer("أنت غير مسجل اطلب من ممثل المرحلة أضافتك", reply_markup=get_user_markup(message.from_user.id))
    else:
        if get_extra_files_list(check_user_stage(message.from_user.id)):
            await GetFile.temp.set()
        await message.answer("اختر كتاب من القائمة", reply_markup=extra_file_markup(get_extra_files_list(check_user_stage(message.from_user.id))))


async def cancel_handler(message, state):
    try:
        # Cancel state
        await state.finish()
        await message.reply('تم الغاء الادخال', reply_markup=get_user_markup(message.from_user.id))
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "main - input canceler ", e)


async def back_to_main_menu(message, state):
    try:
        if not user_manager.check_user_exist(message.from_user.id):
            await bot.send_message(message.chat.id, "أنت غير مسجل اطلب من ممثل المرحلة أضافتك",
                                   reply_markup=get_user_markup(message.from_user.id))
        else:
            await message.reply("تم الرجوع الى القائمة الرئيسية", reply_markup=get_user_markup(message.from_user.id))
            await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "main - back to main menu message handler for view files", e)


async def back_to_main_menu_book(message, state):
    try:
        if not user_manager.check_user_exist(message.from_user.id):
            await bot.send_message(message.chat.id, "أنت غير مسجل اطلب من ممثل المرحلة أضافتك",
                                   reply_markup=get_user_markup(message.from_user.id))
        else:
            await message.reply("تم الرجوع الى القائمة الرئيسية", reply_markup=get_user_markup(message.from_user.id))
            await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "main - back to main menu message handler for view book", e)


async def back_to_mainmenu(message):
    try:
        if not user_manager.check_user_exist(message.from_user.id):
            await bot.send_message(message.chat.id, "أنت غير مسجل اطلب من ممثل المرحلة أضافتك",
                                   reply_markup=get_user_markup(message.from_user.id))
        else:
            await message.reply("تم الرجوع الى القائمة الرئيسية", reply_markup=get_user_markup(message.from_user.id))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "main - back to mainmenu message handler for view book", e)


async def main_menu(message):
    try:
        if not user_manager.check_user_exist(message.from_user.id):
            await bot.send_message(message.chat.id, "أنت غير مسجل اطلب من ممثل المرحلة أضافتك",
                                   reply_markup=get_user_markup(message.from_user.id))
        else:
            await message.reply("تم الرجوع الى القائمة الرئيسية", reply_markup=get_user_markup(message.from_user.id))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "main - back to main menu message handler", e)


async def my_info_message(message):
    try:
        await message.reply(myInfo(message))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "main - my info message", e)


async def cancel_message(message):
    try:
        await message.answer("تم أغلاق القائمة\nلعرض القائمة من جديد ارسل بدء أو اضغط على /start",
                             reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "main - exit message handler", e)


def reg(dp):
    dp.register_message_handler(main_menu, text="الرجوع للقائمة الرئيسية 🏠")
    dp.register_message_handler(back_to_mainmenu, text="الرجوع للقائمة الرئيسية")
    dp.register_message_handler(back_to_main_menu_book, text="الرجوع للقائمة الرئيسية", state=GetBook.temp)
    dp.register_message_handler(back_to_main_menu, text="الرجوع للقائمة الرئيسية", state=GetFile.temp)
    dp.register_message_handler(cancel_handler, text="الغاء الادخال", state='*')
    dp.register_message_handler(View_manager_list, text="عرض صلاحيات المشرف 💂")
    dp.register_message_handler(View_admin_list, text="عرض صلاحيات الادمن 👮")
    dp.register_message_handler(View_hw_menu, text="عرض الواجبات 📃")
    dp.register_message_handler(tools_menu, text="أدوات 🧰")
    dp.register_message_handler(Books_View, text="الكتب 📚")
    dp.register_message_handler(Extra_file_View, text="الملفات 📎")
    dp.register_message_handler(my_info_message, text="معلوماتي ❓")
    dp.register_message_handler(cancel_message, text="أغلاق ❌")

