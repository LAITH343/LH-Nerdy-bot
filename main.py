import logging
import os
import string
import random
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentTypes
from sources.s import answer
from cmds.myinfo import myInfo
from cmds.hw_adder import add_hw
from cmds.hw_getter import get_hw, get_hw_allweek
from cmds import user_manager, error_reporter
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from cmds.classes import AddManager, DelManager, AddHW, DelHW, Anno, AnnoAll, Viewhw, MergePdf, MergeImages, AddNewFile, Del_File, Selcet_Stage, AddNewExtraFile, Del_Extra_File, GetBook, GetFile
from cmds.markup_manager import get_user_markup, manager_markup, admin_markup, custom_markup
from cmds.pdf_manager import merge_pdfs, images_to_pdf
from commands_handlers.unkown_message_handler import unknow_messages
from commands_handlers import tools_handler, main_menu_handler, admin_menu_handler, manager_menu_handler, view_hw_handler, new_user_handler
from cmds.books_manager import get_files_list, get_file_by_name, get_extra_file_by_name, get_extra_files_list


# handle heroku dotenv not found and fails to get the token
try:
    from dotenv import load_dotenv
    # load .env file
    load_dotenv()
    # import bot token from .env file
    bot_token = os.getenv('BOT_TOKEN')
except:
    bot_token = os.environ.get('BOT_TOKEN')


# Configure logging
logging.basicConfig(level=logging.INFO)
# create memory storage for dipatcher
storage = MemoryStorage()

# Initialize bot and dispatcher
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=storage)


# create s exams menu 
s_markup = custom_markup(["جدول المرحلة الاولى", "جدول المرحلة الثانية", "جدول المرحلة الثالثة", "جدول المرحلة الرابعة", "الرجوع للقائمة الرئيسية 🏠"])


# create compress markup
# compress_markup = custom_markup(["الغاء الضغط"])

# add new user
@dp.message_handler(state=Selcet_Stage.stage)
async def Add_new_user(message: types.Message, state: FSMContext):
    await new_user_handler.Add_user(message, state, bot)
    
# create select stage menu 
@dp.message_handler(lambda message: message.text == "اختيار المرحلة")
async def stage_select_menu(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "لا يمكنك الاختيار أنت مسجل مسبقا", reply_markup=get_user_markup(message.from_user.id))
    else:
        await new_user_handler.Select_stage(message, bot)


# create start message/command handler
@dp.message_handler(lambda message: message.text in ["start", "بدء", "/start"])
async def start_message(message: types.Message):
    await bot.send_message(message.chat.id, "أهلا بك في البوت", reply_markup=get_user_markup(message.from_user.id))

# create exit message handler
@dp.message_handler(lambda message: message.text == "أغلاق ❌")
async def cancel_message(message: types.Message):
    await message.answer("تم أغلاق القائمة\nلعرض القائمة من جديد ارسل بدء أو اضغط على /start", reply_markup=types.ReplyKeyboardRemove())

# create view book handler
@dp.message_handler(lambda message: message.text == "الكتب 📚")
async def view_books(message: types.Message):
    await main_menu_handler.Books_View(message)

# create view extra files handler
@dp.message_handler(lambda message: message.text == "الملفات 📎")
async def view_books(message: types.Message):
    await main_menu_handler.Extra_file_View(message)


# create delete book canceler
@dp.message_handler(lambda message: message.text == "الغاء الحذف" ,state=Del_File)
async def cancel_del_book(message: types.Message, state: FSMContext):
    if user_manager.get_manager_stage(message.from_user.id) == False:
        await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
    else:
        await state.finish()
        await message.answer("تم الالغاء بنجاح", reply_markup=get_user_markup(message.from_user.id))

# create delete book 
@dp.message_handler(lambda message: message.text == "حذف كتاب ❌")
async def del_book_handler(message: types.Message):
    await manager_menu_handler.del_book(message, bot)

# create delete book by name handler
@dp.message_handler(state=Del_File.temp)
async def del_book_command_handler(message: types.Message, state: FSMContext):
    await manager_menu_handler.del_book_command(message, state, bot)

# create delete extra file canceler
@dp.message_handler(lambda message: message.text == "الغاء حذف الملف" ,state=Del_Extra_File)
async def cancel_del_book(message: types.Message, state: FSMContext):
    if user_manager.get_manager_stage(message.from_user.id) == False:
        await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
    else:
        await state.finish()
        await message.answer("تم الالغاء بنجاح", reply_markup=get_user_markup(message.from_user.id))

# create delete extra file 
@dp.message_handler(lambda message: message.text == "حذف ملف ❌")
async def del_book_handler(message: types.Message):
    await manager_menu_handler.Del_extra_file(message, bot)

# create delete extra file by name handler
@dp.message_handler(state=Del_Extra_File.temp)
async def del_book_command_handler(message: types.Message, state: FSMContext):
    await manager_menu_handler.del_extra_file_command(message, state, bot)

# create upload book handler
@dp.message_handler(lambda message: message.text in get_files_list(user_manager.check_user_stage(message.from_user.id)), state=GetBook.temp)
async def upload_book(message: types.Message, state: FSMContext):
    try:
        await message.answer("جاري رفع الكتاب", reply_markup=get_user_markup(message.from_user.id))
        await bot.send_document(message.chat.id, document=open(get_file_by_name(user_manager.check_user_stage(message.from_user.id), message.text), 'rb'))
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "main - upload book handler", e)

# create upload extra handler
@dp.message_handler(lambda message: message.text in get_extra_files_list(user_manager.check_user_stage(message.from_user.id)), state=GetFile.temp)
async def upload_book(message: types.Message, state: FSMContext):
    try:
        await message.answer("جاري رفع الملف", reply_markup=get_user_markup(message.from_user.id))
        await bot.send_document(message.chat.id, document=open(get_extra_file_by_name(user_manager.check_user_stage(message.from_user.id), message.text), 'rb'))
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "main - upload extra handler", e)

# create tools option at main meun 
@dp.message_handler(lambda message: message.text == "أدوات 🧰")
async def tools(message: types.Message):
    await main_menu_handler.tools_menu(message, bot)

# create add book cancler
@dp.message_handler(lambda message: message.text == 'الغاء الاضافة', state=AddNewFile)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    await message.reply('تم الغاء الاضافة', reply_markup=get_user_markup(message.from_user.id))

# create add extra file cancler
@dp.message_handler(lambda message: message.text == 'الغاء الاضافة', state=AddNewExtraFile)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    await message.reply('تم الغاء الاضافة', reply_markup=get_user_markup(message.from_user.id))

# create add book 
@dp.message_handler(lambda message: message.text == "اضافة كتاب 📕")
async def pdf_message(message: types.Message):
    await manager_menu_handler.Add_book(message, bot)

# get file name
@dp.message_handler(state=AddNewFile.file_name)
async def Add_file_get_name(message: types.Message, state: FSMContext):
    await manager_menu_handler.Add_book_get_file_name(message, state, bot)

# download file
@dp.message_handler(state=AddNewFile.file_path, content_types=ContentTypes.DOCUMENT)
async def Add_file_download(message: types.Message, state: FSMContext):
    await manager_menu_handler.Add_book_command(message, state, bot)

# create add file command
# create add file cancler
@dp.message_handler(lambda message: message.text == 'الغاء الاضافة', state=AddNewFile)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    await message.reply('تم الغاء الاضافة', reply_markup=get_user_markup(message.from_user.id))

# create add file 
@dp.message_handler(lambda message: message.text == "اضافة ملف 📎")
async def pdf_message(message: types.Message):
    await manager_menu_handler.Add_extra_file(message, bot)

# get file name
@dp.message_handler(state=AddNewExtraFile.file_name)
async def Add_file_get_name(message: types.Message, state: FSMContext):
    await manager_menu_handler.Add_extra_file_get_file_name(message, state, bot)

# download file
@dp.message_handler(state=AddNewExtraFile.file_path, content_types=ContentTypes.DOCUMENT)
async def Add_file_download(message: types.Message, state: FSMContext):
    await manager_menu_handler.Add_extra_file_command(message, state, bot)

#create my info message
@dp.message_handler(lambda message: message.text == "معلوماتي ❓")
async def my_info_message(message: types.Message):
    await message.reply(myInfo(message))

# create back to main menu message handler
@dp.message_handler(lambda message: message.text == "الرجوع للقائمة الرئيسية 🏠")
async def back_to_main_menu(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
    else:
        await message.reply("تم الرجوع الى القائمة الرئيسية", reply_markup=get_user_markup(message.from_user.id))

# create back to main menu message handler for view book
@dp.message_handler(lambda message: message.text == "الرجوع للقائمة الرئيسية", state=GetBook.temp)
async def back_to_main_menu(message: types.Message, state: FSMContext):
    if user_manager.check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
    else:
        await message.reply("تم الرجوع الى القائمة الرئيسية", reply_markup=get_user_markup(message.from_user.id))
        await state.finish()

# create back to main menu message handler for view files
@dp.message_handler(lambda message: message.text == "الرجوع للقائمة الرئيسية", state=GetFile.temp)
async def back_to_main_menu(message: types.Message, state: FSMContext):
    if user_manager.check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
    else:
        await message.reply("تم الرجوع الى القائمة الرئيسية", reply_markup=get_user_markup(message.from_user.id))
        await state.finish()


# create hw messages menu 
@dp.message_handler(lambda message: message.text == "عرض الواجبات 📃")
async def view_hw(message: types.Message):
    await main_menu_handler.View_hw_menu(message, bot)


# create delete user command handler
@dp.message_handler(commands='deluser')
async def user_managment(message: types.Message):
    if user_manager.check_admin(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
    else:
        m = message.get_full_command()
        if user_manager.del_user(m[1]) == True:
            await message.reply("تم الحذف بنجاح")
        else:
            await message.reply("حدث خطأ عند الحذف")

# create photos menu stage
@dp.message_handler(lambda message: message.text == "الصور 📷")
async def pics(message: types.Message):
    await main_menu_handler.View_pic_menu(message, bot)


# create input canceler 
@dp.message_handler(state='*', commands='الغاء الادخال')
@dp.message_handler(Text(equals='الغاء الادخال', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    await message.reply('تم الغاء الادخال', reply_markup=get_user_markup(message.from_user.id))

# create hw all week message handler
@dp.message_handler(lambda message: message.text == "عرض واجبات الاسبوع 📖")
async def view_hw(message: types.Message):
    await view_hw_handler.View_hw_all_command(message, bot)

# create view hw message handler
@dp.message_handler(lambda message: message.text == "اختيار يوم 📋")
async def select_hw(message: types.Message):
    await view_hw_handler.View_hw_select_day(message, bot)

@dp.message_handler(state=Viewhw.day)
async def view_by_day(message: types.Message, state=Viewhw):
    await view_hw_handler.View_hw_command(message, state, bot)

# create add HW command handler
@dp.message_handler(lambda message: message.text == 'اضافة واجب 📝')
async def HW_managment(message: types.Message):
    await manager_menu_handler.Manager_add_hw(message, bot)

# get the day from the user
@dp.message_handler(state=AddHW.day)
async def process_day(message: types.Message, state: FSMContext):
    await manager_menu_handler.Manager_get_day(message, state, bot)

# get add hw message handler
@dp.message_handler(state=AddHW.hw)
async def process_age(message: types.Message, state: FSMContext):
    await manager_menu_handler.Manager_add_hw_command(message, state, bot)


# create delete HW command handler
@dp.message_handler(lambda message: message.text == 'حذف واجب 📝')
async def HW_managment(message: types.Message):
    await manager_menu_handler.Manager_del_hw(message, bot)

# get the day from the user
@dp.message_handler(state=DelHW.day)
async def process_day(message: types.Message, state: FSMContext):
    await manager_menu_handler.Manager_del_hw_command(message, state, bot)

# send announcement for a stage by manager
@dp.message_handler(lambda message: message.text == 'أرسال اعلان 📢')
async def anno_managment(message: types.Message):
    await manager_menu_handler.Manager_send_anno(message, bot)

# get the message from the manager and send it to the student
@dp.message_handler(state=Anno.m)
async def process_message(message: types.Message, state: FSMContext):
    await manager_menu_handler.Manager_send_anno_command(message, state, bot)

# create add manager command handler
@dp.message_handler(lambda message: message.text == 'اضافة مشرف 💂')
async def user_managment(message: types.Message):
    await admin_menu_handler.Add_manager(message, bot)

# get the stage from the user
@dp.message_handler(state=AddManager.stage)
async def process_name(message: types.Message, state: FSMContext):
    await admin_menu_handler.Add_manager_get_stage(message, state, bot)

# get user id form the user and end data entry
@dp.message_handler(lambda message: message.text.isdigit(), state=AddManager.uid)
async def process_age(message: types.Message, state: FSMContext):
    await admin_menu_handler.Add_manager_get_uid_and_add(message, state, bot)



# create delete manager command handler
@dp.message_handler(lambda message: message.text == 'حذف مشرف 💂')
async def user_managment(message: types.Message):
    await admin_menu_handler.Delete_manager(message, bot)

# get the stage from the user
@dp.message_handler(state=DelManager.stage)
async def process_name(message: types.Message, state: FSMContext):
    await admin_menu_handler.Delete_manager_get_stage(message, state)

# get user id form the user and end data entry
@dp.message_handler(lambda message: message.text.isdigit(), state=DelManager.uid)
async def process_age(message: types.Message, state: FSMContext):
    await admin_menu_handler.Delete_manager_get_uid_and_del(message, state, bot)

# send announcement for all stages by admin
@dp.message_handler(lambda message: message.text == 'أرسال اعلان للجميع 📢')
async def anno_managment(message: types.Message):
    await admin_menu_handler.Send_anno_4all(message, bot)

# get the message from the manager and send it to the student
@dp.message_handler(state=AnnoAll.m)
async def process_message(message: types.Message, state: FSMContext):
    await admin_menu_handler.Get_anno_msg_and_send(message, state, bot)

# create list of user id and username for all users 
@dp.message_handler(lambda message: message.text == "عرض جميع المستخدمين 📋")
async def make_list(message: types.Message):
    await admin_menu_handler.View_all_users(message, bot)

# create admin permissions list getter 
@dp.message_handler(lambda message: message.text == "عرض صلاحيات الادمن 👮")
async def view_admin_permissions(message: types.Message):
    await main_menu_handler.View_admin_list(message)


# create manager premissions list getter 
@dp.message_handler(lambda message: message.text == "عرض صلاحيات المشرف 💂")
async def view_man_permissions(message: types.Message):
    await main_menu_handler.View_manager_list(message)

# create merge pdfs message handler
# create merge pdf canceler handler
@dp.message_handler(lambda message: message.text == "الغاء الدمج", state=MergePdf)
async def merge(message: types.Message, state: FSMContext):
    await tools_handler.MergePdf_cancel_handler(message, state, bot)

# ask the user about the file name
@dp.message_handler(lambda message: message.text == "دمج ملفات pdf")
async def merge_file_name(message: types.Message, state: FSMContext):
    await tools_handler.MergePdf_ask_file_name(message, state, bot)

# get the file name
@dp.message_handler(state=MergePdf.file_name)
async def get_file_name(message: types.Message, state: FSMContext):
    await tools_handler.MergePdf_get_file_name(message, state, bot)


# create pdfs getter
@dp.message_handler(state=MergePdf.temp, content_types=ContentTypes.DOCUMENT)
async def pdf_getter(message: types.Message, state: FSMContext):
    await tools_handler.MergePdf_get_files(message, state, bot)

# create merge pdf command handler
@dp.message_handler(lambda message: message.text == "دمج" ,state=MergePdf.temp)
async def merge_handler(message: types.Message, state: FSMContext):
    await tools_handler.MergePdf_merge(message, state, bot)

# create images to pdf message handler
# create cancel images merge to pdf message handler
@dp.message_handler(lambda message: message.text == "الغاء الدمج", state=MergeImages)
async def merge(message: types.Message, state: FSMContext):
    await tools_handler.Imgs2Pdf_cancel_handler(message, state, bot)


# ask the user about the name of the file
@dp.message_handler(lambda message: message.text == "تحويل الصور الى pdf")
async def merge(message: types.Message, state: FSMContext):
    await tools_handler.Imgs2Pdf_file_name(message, state, bot)


# get the images from the user
@dp.message_handler(state=MergeImages.file_name)
async def merge(message: types.Message, state: FSMContext):
    await tools_handler.Imgs2Pdf_get_images(message, state, bot)

# create merge images command handler
@dp.message_handler(lambda message: message.text == "دمج" ,state=MergeImages.temp)
async def merge(message: types.Message, state: FSMContext):
    await tools_handler.Imgs2Pdf_merge_handler(message, state, bot)

# create images downloader
@dp.message_handler(state=MergeImages.temp, content_types=ContentTypes.ANY)
async def images_downloader(message: types.Message, state: FSMContext):
    await tools_handler.Imgs2Pdf_Imgs_downloader(message, state, bot)


# create unkown message handler
@dp.message_handler()
async def unknow(message: types.Message):
    loop = asyncio.get_event_loop()
    await unknow_messages(message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)