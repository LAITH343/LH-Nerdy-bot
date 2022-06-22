import logging
import os
import string
import random
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentTypes, MenuButtonDefault
from telegram import MenuButton

from sources.s import answer
from sources.pdfs_links import links
from cmds.myinfo import myInfo
from cmds.hw_adder import add_hw
from cmds.hw_getter import get_hw, get_hw_allweek
from cmds import user_manager
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from cmds.classes import AddManager, DelManager, AddHW, DelHW, Anno, AnnoAll, Viewhw, MergePdf, MergeImages
from cmds.markup_manager import get_user_markup, manager_markup, admin_markup, custom_markup
from cmds.pdf_manager import merge_pdfs, images_to_pdf
from commands_handlers.unkown_message_handler import unknow_messages
from commands_handlers import tools_handler, main_menu_handler, admin_menu_handler, manager_menu_handler, view_hw_handler
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


# create stages menu 
stages_markup = custom_markup(["مرحلة اولى","مرحلة ثانية","مرحلة ثالثة","مرحلة رابعة"])



# create compress markup
# compress_markup = custom_markup(["الغاء الضغط"])

# set new user stage
@dp.message_handler(lambda message: message.text == "مرحلة اولى")
async def stage_select(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "لا يمكنك الاختيار أنت مسجل مسبقا", reply_markup=get_user_markup(message.from_user.id))
    else:
        if user_manager.add_user("stage1", message.from_user.id, message.from_user.username) == True:
            await bot.send_message(message.chat.id, "تم الاضافة", reply_markup=get_user_markup(message.from_user.id))
        else:
            await bot.send_message(message.chat.id, "فشل الاضافة", reply_markup=stages_markup)

@dp.message_handler(lambda message: message.text == "مرحلة ثانية")
async def stage_select(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "لا يمكنك الاختيار أنت مسجل مسبقا", reply_markup=get_user_markup(message.from_user.id))
    else:
        if user_manager.add_user("stage2", message.from_user.id, message.from_user.username) == True:
            await bot.send_message(message.chat.id, "تم الاضافة", reply_markup=get_user_markup(message.from_user.id))
        else:
            await bot.send_message(message.chat.id, "فشل الاضافة", reply_markup=stages_markup)

@dp.message_handler(lambda message: message.text == "مرحلة ثالثة")
async def stage_select(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "لا يمكنك الاختيار أنت مسجل مسبقا", reply_markup=get_user_markup(message.from_user.id))
    else:
        if user_manager.add_user("stage3", message.from_user.id, message.from_user.username) == True:
            await bot.send_message(message.chat.id, "تم الاضافة", reply_markup=get_user_markup(message.from_user.id))
        else:
            await bot.send_message(message.chat.id, "فشل الاضافة", reply_markup=stages_markup)

@dp.message_handler(lambda message: message.text == "مرحلة رابعة")
async def stage_select(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "لا يمكنك الاختيار أنت مسجل مسبقا", reply_markup=get_user_markup(message.from_user.id))
    else:
        if user_manager.add_user("stage4", message.from_user.id, message.from_user.username) == True:
            await bot.send_message(message.chat.id, "تم الاضافة", reply_markup=get_user_markup(message.from_user.id))
        else:
            await bot.send_message(message.chat.id, "فشل الاضافة", reply_markup=stages_markup)
    
# create select stage menu 
@dp.message_handler(lambda message: message.text == "اختيار المرحلة")
async def stage_select_menu(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "لا يمكنك الاختيار أنت مسجل مسبقا", reply_markup=get_user_markup(message.from_user.id))
    else:
        await bot.send_message(message.chat.id, "اختر المرحلة\nملاحظة مهمة: يمكنك اختيار المرحلة لمرة واحدة فقط", reply_markup=stages_markup)


# create start message/command handler
@dp.message_handler(lambda message: message.text in ["start", "بدء", "/start"])
async def start_message(message: types.Message):
    await bot.send_message(message.chat.id, "أهلا بك في البوت", reply_markup=get_user_markup(message.from_user.id))

# create tools option at main meun 
@dp.message_handler(lambda message: message.text == "أدوات 🧰")
async def tools(message: types.Message):
    await main_menu_handler.tools_menu(message, bot)

# create pdf menu 
@dp.message_handler(lambda message: message.text == "ملازم 📚")
async def pdf_message(message: types.Message):
    await main_menu_handler.View_pdf_menu(message, bot)

#create my info message
@dp.message_handler(lambda message: message.text == "معلوماتي ❓")
async def my_info_message(message: types.Message):
    await message.reply(myInfo(message))

# create exit message handler
@dp.message_handler(lambda message: message.text == "أغلاق ❌")
async def cancel_message(message: types.Message):
    await message.reply("تم أغلاق القائمة\nلعرض القائمة من جديد ارسل بدء أو اضغط على /start", reply_markup=types.ReplyKeyboardRemove())

# create collage logo message handler
@dp.message_handler(lambda message: message.text == "شعار الكلية")
async def duc_logo(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("جاري رفع الصورة... يرجى الانتظار")
        await bot.send_photo(message.chat.id, types.InputFile.from_url('https://duc.edu.iq/wp-content/uploads/2020/04/unnamed-file-1.png'))

# create cs department logo message handler
@dp.message_handler(lambda message: message.text == "شعار القسم")
async def dep_logo(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("جاري رفع الصورة... يرجى الانتظار")
        await bot.send_photo(message.chat.id, types.InputFile.from_url('https://api.portal.duc.edu.iq/uploads/view/1645104654002.png'))

# create s exams menu 
@dp.message_handler(lambda message: message.text == "جدول الامتحانات")
async def s_menu(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await bot.send_message(message.chat.id, "يمكنك الاختيار لعرض الجدول", reply_markup=s_markup)

# create first stage s exams message handler 
@dp.message_handler(lambda message: message.text == "جدول المرحلة الاولى")
async def s_stage1(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply(answer("جدول المرحلة الاولى"))

# create second stage s exams message handler 
@dp.message_handler(lambda message: message.text == "جدول المرحلة الثانية")
async def s_stage2(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply(answer("جدول المرحلة الثانية"))


# create third stage s exams message handler 
@dp.message_handler(lambda message: message.text == "جدول المرحلة الثالثة")
async def s_stage3(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply(answer("جدول المرحلة الثالثة"))


# create fourth stage s exams message handler 
@dp.message_handler(lambda message: message.text == "جدول المرحلة الرابعة")
async def s_stage4(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply(answer("جدول المرحلة الرابعة"))

# create back to main menu message handler
@dp.message_handler(lambda message: message.text == "الرجوع للقائمة الرئيسية 🏠")
async def back_to_main_menu(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("تم الرجوع الى القائمة الرئيسية", reply_markup=get_user_markup(message.from_user.id))

# create logic pdf message handler
@dp.message_handler(lambda message: message.text == "منطق رقمي")
async def pdf_message(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("جاري الرفع... ")
        await bot.send_document(message.chat.id, links("logic"))

# create c++ pdf message handler
@dp.message_handler(lambda message: message.text == "برمجة سي بلس بلس 2")
async def pdf_message(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("جاري الرفع... ")
        await bot.send_document(message.chat.id, links("cplusplus"))

# create pf pdf message handler
@dp.message_handler(lambda message: message.text == "اساسيات البرمجة")
async def pdf_message(message: types.Message):
    if user_manager.check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("جاري الرفع... ")
        await bot.send_document(message.chat.id, links("pf"))


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
        values = m[1].split(" ")
        if user_manager.del_user(values[0], int(values[1])) == True:
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
    await manager_menu_handler.Manager_get_day(message, state)

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
    await admin_menu_handler.Add_manager_get_stage(message, state)

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
    await tools_handler.MergePdf_cancel_handler(message, state)

# ask the user about the file name
@dp.message_handler(lambda message: message.text == "دمج ملفات pdf")
async def merge_file_name(message: types.Message, state: FSMContext):
    await tools_handler.MergePdf_ask_file_name(message, state)

# get the file name
@dp.message_handler(state=MergePdf.file_name)
async def get_file_name(message: types.Message, state: FSMContext):
    await tools_handler.MergePdf_get_file_name(message, state, bot)


# create pdfs getter
@dp.message_handler(state=MergePdf.temp, content_types=ContentTypes.DOCUMENT)
async def pdf_getter(message: types.Message, state: FSMContext):
    await tools_handler.MergePdf_get_files(message, state)

# create merge pdf command handler
@dp.message_handler(lambda message: message.text == "دمج" ,state=MergePdf.temp)
async def merge_handler(message: types.Message, state: FSMContext):
    await tools_handler.MergePdf_merge(message, state, bot)

# create images to pdf message handler
# create cancel images merge to pdf message handler
@dp.message_handler(lambda message: message.text == "الغاء الدمج", state=MergeImages)
async def merge(message: types.Message, state: FSMContext):
    await tools_handler.Imgs2Pdf_cancel_handler(message, state)


# ask the user about the name of the file
@dp.message_handler(lambda message: message.text == "تحويل الصور الى pdf")
async def merge(message: types.Message, state: FSMContext):
    await tools_handler.Imgs2Pdf_file_name(message, state)


# get the images from the user
@dp.message_handler(state=MergeImages.file_name)
async def merge(message: types.Message, state: FSMContext):
    await tools_handler.Imgs2Pdf_get_images(message, state)


# create images downloader
@dp.message_handler(state=MergeImages.temp, content_types=ContentTypes.DOCUMENT)
async def images_downloader(message: types.Message, state: FSMContext):
    await tools_handler.Imgs2Pdf_Imgs_downloader(message, state)
    

# create merge images command handler
@dp.message_handler(lambda message: message.text == "دمج" ,state=MergeImages.temp)
async def merge(message: types.Message, state: FSMContext):
    await tools_handler.Imgs2Pdf_merge_handler(message, state, bot)


"""
# create pdf compress handler
@dp.message_handler(lambda message: message.text == "ضغط ملف pdf (تقليل حجم)")
async def merge(message: types.Message, state: FSMContext):
    if check_user_exist(message.from_user.id) == False:
        await message.reply("اختر المرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
    else:
        await CompressPdf.folder.set()
        randfile = ''.join(random.choice(string.ascii_lowercase) for i in range(20))
        os.system(f"mkdir cache/{randfile}")
        async with state.proxy() as data:
            data['folder'] = f"cache/{randfile}"
        await message.reply("ارسل ملف الpdf", reply_markup=compress_markup)

# create compress cancel message handler
@dp.message_handler(lambda message: message.text == "الغاء الضغط", state=CompressPdf.folder)
async def compress_cancel(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        os.system(f"rm -rf {data['folder']}")
        await message.reply("تم الغاء الضغط وحذف الملفات", reply_markup=get_user_markup(message.from_user.id))
    await state.finish()

# download the file and re-send it after compresing
@dp.message_handler(state=CompressPdf.folder, content_types=ContentTypes.DOCUMENT)
async def download_and_upload(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if document := message.document:
            await bot.send_message(message.chat.id, "جاري تنزيل الملف يرجى الانتضار")
            await document.download(
                destination_file=f"{data['folder']}/{document.file_name}",
            )
            await bot.send_message(message.chat.id, "جاري ضغط الملف يرجى الانتضار")
            await bot.send_document(message.chat.id, document=open(compress_pdf(f"{data['folder']}/{document.file_name}", data['folder']), 'rb'), reply_markup=get_user_markup(message.from_user.id))
                # await message.reply("فشل دمج الملفات")
            os.system(f"rm -rf {data['folder']}")
        await state.finish()
"""

# create unkown message handler
@dp.message_handler()
async def unknow(message: types.Message):
    loop = asyncio.get_event_loop()
    await unknow_messages(message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)