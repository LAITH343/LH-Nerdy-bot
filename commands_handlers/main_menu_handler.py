import asyncio
from aiogram import types
from cmds.markup_manager import manager_markup, admin_markup, get_user_markup, custom_markup, books_markup, extra_file_markup
from cmds.user_manager import check_admin, check_user_exist, get_manager_stage, check_user_stage
from cmds.classes import AddNewFile, GetBook, GetFile
from cmds.books_manager import add_file, get_files_list, get_extra_files_list
async def View_manager_list(message):
    if get_manager_stage(message.from_user.id) != False:
        await message.reply("تم عرض صلاحيات المشرف", reply_markup=manager_markup())
    else:
        await message.reply("ليس لديك الصلاحية لعرض هذه القائمة", reply_markup=get_user_markup(message.from_user.id))

async def View_admin_list(message):
    if check_admin(message.from_user.id) == True:
        await message.reply("تم عرض صلاحيات الادمن", reply_markup=admin_markup())
    else:
        await message.reply("ليس لديك الصلاحية لعرض هذه القائمة", reply_markup=get_user_markup(message.from_user.id))

async def View_pic_menu(message, bot):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
    else:
        await bot.send_message(message.chat.id, "اختر من الصور", reply_markup=custom_markup(["شعار القسم","شعار الكلية","الرجوع للقائمة الرئيسية 🏠"]))

async def View_hw_menu(message, bot):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
    else:
        await bot.send_message(message.chat.id, "اختر اليوم من القائمة", reply_markup=custom_markup(["اختيار يوم 📋","عرض واجبات الاسبوع 📖","الرجوع للقائمة الرئيسية 🏠"]))

async def View_pdf_menu(message, bot):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
    else:
        await bot.send_message(message.chat.id, "اختر الملف من القائمة", reply_markup=custom_markup(["منطق رقمي", "برمجة سي بلس بلس 2", "اساسيات البرمجة", "الرجوع للقائمة الرئيسية 🏠"]))

async def tools_menu(message, bot):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "يرجى اختيار المرحلة اولا")
    else:
        await message.reply("أختر من القائمة", reply_markup=custom_markup(["دمج ملفات pdf","تحويل الصور الى pdf","الرجوع للقائمة الرئيسية 🏠"]))


async def Books_View(message):
    if check_user_exist(message.from_user.id) == False:
        message.answer("يجب اختيار مرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
    else:
        if get_files_list(check_user_stage(message.from_user.id)) != []:
            await GetBook.temp.set()
        await message.answer("اختر كاتب من القائمة", reply_markup=books_markup(get_files_list(check_user_stage(message.from_user.id))))

async def Extra_file_View(message):
    if check_user_exist(message.from_user.id) == False:
        message.answer("يجب اختيار مرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
    else:
        if get_extra_files_list(check_user_stage(message.from_user.id)) != []:
            await GetFile.temp.set()
        await message.answer("اختر كاتب من القائمة", reply_markup=extra_file_markup(get_extra_files_list(check_user_stage(message.from_user.id))))