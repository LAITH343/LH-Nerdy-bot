import logging
import os
import string
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentTypes

from sources.s import answer
from sources.pdfs_links import links
from cmds.myinfo import myInfo
from cmds.hw_adder import add_hw
from cmds.hw_getter import get_hw, get_hw_allweek
from cmds.user_manager import check_user_stage, add_user, del_user, check_user_exist, check_admin, add_manager, del_manager, get_manager_stage, get_users_uid, get_users_uid_all, get_all_users_username
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from cmds.classes import AddManager, DelManager, AddHW, DelHW, Anno, AnnoAll, Viewhw, MergePdf, MergeImages
from cmds.markup_manager import get_user_markup, manager_markup, admin_markup
from cmds.pdf_manager import merge_pdfs, images_to_pdf

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

# create pdf files menu
pdf_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
pdf_markup.add("منطق رقمي")
pdf_markup.add("برمجة سي بلس بلس 2")
pdf_markup.add("اساسيات البرمجة")
pdf_markup.add("الرجوع للقائمة الرئيسية 🏠")

# create s exams menu 
s_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
s_markup.add("جدول المرحلة الاولى")
s_markup.add("جدول المرحلة الثانية")
s_markup.add("جدول المرحلة الثالثة")
s_markup.add("جدول المرحلة الرابعة")
s_markup.add("الرجوع للقائمة الرئيسية 🏠")

# create hw menu 
hw_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
hw_markup.add("اختيار يوم 📋")
hw_markup.add("عرض واجبات الاسبوع 📖")
hw_markup.add("الرجوع للقائمة الرئيسية 🏠")

# create stages menu 
stages_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
stages_markup.add("مرحلة اولى")
stages_markup.add("مرحلة ثانية")
stages_markup.add("مرحلة ثالثة")
stages_markup.add("مرحلة رابعة")

# create photos menu 
pic_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
pic_markup.add("شعار القسم")
pic_markup.add("شعار الكلية")
pic_markup.add("الرجوع للقائمة الرئيسية 🏠")

# create cancel input markup
cancel_input_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
cancel_input_markup.add("الغاء الادخال")

# create hw day input markup
hw_day_input_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
hw_day_input_markup.add("الاحد")
hw_day_input_markup.add("الاثنين")
hw_day_input_markup.add("الثلاثاء")
hw_day_input_markup.add("الاربعاء")
hw_day_input_markup.add("الخميس")
hw_day_input_markup.add("الغاء الادخال")

# create select stage for add/delete manager input markup
add_del_man_stage_input_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
add_del_man_stage_input_markup.add("stage1")
add_del_man_stage_input_markup.add("stage2")
add_del_man_stage_input_markup.add("stage3")
add_del_man_stage_input_markup.add("stage4")
add_del_man_stage_input_markup.add("الغاء الادخال")

# create merge markup
merge_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
merge_markup.add("دمج")
merge_markup.add("الغاء الدمج")

# create compress markup
compress_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
compress_markup.add("الغاء الضغط")

# set new user stage
@dp.message_handler(lambda message: message.text == "مرحلة اولى")
async def stage_select(message: types.Message):
    if check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "لا يمكنك الاختيار أنت مسجل مسبقا", reply_markup=get_user_markup(message.from_user.id))
    else:
        if add_user("stage1", message.from_user.id, message.from_user.username) == True:
            await bot.send_message(message.chat.id, "تم الاضافة", reply_markup=get_user_markup(message.from_user.id))
        else:
            await bot.send_message(message.chat.id, "فشل الاضافة", reply_markup=stages_markup)

@dp.message_handler(lambda message: message.text == "مرحلة ثانية")
async def stage_select(message: types.Message):
    if check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "لا يمكنك الاختيار أنت مسجل مسبقا", reply_markup=get_user_markup(message.from_user.id))
    else:
        if add_user("stage2", message.from_user.id, message.from_user.username) == True:
            await bot.send_message(message.chat.id, "تم الاضافة", reply_markup=get_user_markup(message.from_user.id))
        else:
            await bot.send_message(message.chat.id, "فشل الاضافة", reply_markup=stages_markup)

@dp.message_handler(lambda message: message.text == "مرحلة ثالثة")
async def stage_select(message: types.Message):
    if check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "لا يمكنك الاختيار أنت مسجل مسبقا", reply_markup=get_user_markup(message.from_user.id))
    else:
        if add_user("stage3", message.from_user.id, message.from_user.username) == True:
            await bot.send_message(message.chat.id, "تم الاضافة", reply_markup=get_user_markup(message.from_user.id))
        else:
            await bot.send_message(message.chat.id, "فشل الاضافة", reply_markup=stages_markup)

@dp.message_handler(lambda message: message.text == "مرحلة رابعة")
async def stage_select(message: types.Message):
    if check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "لا يمكنك الاختيار أنت مسجل مسبقا", reply_markup=get_user_markup(message.from_user.id))
    else:
        if add_user("stage4", message.from_user.id, message.from_user.username) == True:
            await bot.send_message(message.chat.id, "تم الاضافة", reply_markup=get_user_markup(message.from_user.id))
        else:
            await bot.send_message(message.chat.id, "فشل الاضافة", reply_markup=stages_markup)
    
# create select stage menu 
@dp.message_handler(lambda message: message.text == "اختيار المرحلة")
async def stage_select_menu(message: types.Message):
    if check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "لا يمكنك الاختيار أنت مسجل مسبقا", reply_markup=get_user_markup(message.from_user.id))
    else:
        await bot.send_message(message.chat.id, "اختر المرحلة\nملاحظة مهمة: يمكنك اختيار المرحلة لمرة واحدة فقط", reply_markup=stages_markup)


# create start message/command handler
@dp.message_handler(lambda message: message.text in ["start", "بدء", "/start"])
async def start_message(message: types.Message):
    await bot.send_message(message.chat.id, "أهلا بك في البوت", reply_markup=get_user_markup(message.from_user.id))

# create pdf menu 
@dp.message_handler(lambda message: message.text == "ملازم 📚")
async def pdf_message(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await bot.send_message(message.chat.id, "اختر الملف من القائمة", reply_markup=pdf_markup)

#create my info message
@dp.message_handler(lambda message: message.text == "معلوماتي ❓")
async def my_info_message(message: types.Message):
    await message.reply(myInfo(message))

# create exit message handler
@dp.message_handler(lambda message: message.text == "أغلاق ❌")
async def cancel_message(message: types.Message):
    cmarkup = types.ReplyKeyboardRemove()
    await message.reply("تم أغلاق القائمة\nلعرض القائمة من جديد ارسل بدء أو اضغط على /start", reply_markup=cmarkup)

# create collage logo message handler
@dp.message_handler(lambda message: message.text == "شعار الكلية")
async def duc_logo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("جاري رفع الصورة... يرجى الانتظار")
        await bot.send_photo(message.chat.id, types.InputFile.from_url('https://duc.edu.iq/wp-content/uploads/2020/04/unnamed-file-1.png'))

# create cs department logo message handler
@dp.message_handler(lambda message: message.text == "شعار القسم")
async def dep_logo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("جاري رفع الصورة... يرجى الانتظار")
        await bot.send_photo(message.chat.id, types.InputFile.from_url('https://api.portal.duc.edu.iq/uploads/view/1645104654002.png'))

# create s exams menu 
@dp.message_handler(lambda message: message.text == "جدول الامتحانات")
async def s_menu(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await bot.send_message(message.chat.id, "يمكنك الاختيار لعرض الجدول", reply_markup=s_markup)

# create first stage s exams message handler 
@dp.message_handler(lambda message: message.text == "جدول المرحلة الاولى")
async def s_stage1(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply(answer("جدول المرحلة الاولى"))

# create second stage s exams message handler 
@dp.message_handler(lambda message: message.text == "جدول المرحلة الثانية")
async def s_stage2(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply(answer("جدول المرحلة الثانية"))


# create third stage s exams message handler 
@dp.message_handler(lambda message: message.text == "جدول المرحلة الثالثة")
async def s_stage3(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply(answer("جدول المرحلة الثالثة"))


# create fourth stage s exams message handler 
@dp.message_handler(lambda message: message.text == "جدول المرحلة الرابعة")
async def s_stage4(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply(answer("جدول المرحلة الرابعة"))

# create back to main menu message handler
@dp.message_handler(lambda message: message.text == "الرجوع للقائمة الرئيسية 🏠")
async def back_to_main_menu(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("تم الرجوع الى القائمة الرئيسية", reply_markup=get_user_markup(message.from_user.id))

# create logic pdf message handler
@dp.message_handler(lambda message: message.text == "منطق رقمي")
async def pdf_message(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("جاري الرفع... ")
        await bot.send_document(message.chat.id, links("logic"))

# create c++ pdf message handler
@dp.message_handler(lambda message: message.text == "برمجة سي بلس بلس 2")
async def pdf_message(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("جاري الرفع... ")
        await bot.send_document(message.chat.id, links("cplusplus"))

# create pf pdf message handler
@dp.message_handler(lambda message: message.text == "اساسيات البرمجة")
async def pdf_message(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("جاري الرفع... ")
        await bot.send_document(message.chat.id, links("pf"))


# create hw messages menu 
@dp.message_handler(lambda message: message.text == "عرض الواجبات 📃")
async def view_hw(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await bot.send_message(message.chat.id, "اختر اليوم من القائمة", reply_markup=hw_markup)


# create hw all week message handler
@dp.message_handler(lambda message: message.text == "عرض واجبات الاسبوع 📖")
async def view_hw(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        stage = check_user_stage(message.from_user.id)
        if stage == False:
            await message.reply("انت لا تنتمي الى مرحلة")
        else:
            await message.reply(get_hw_allweek(stage))

# create delete user command handler
@dp.message_handler(commands='deluser')
async def user_managment(message: types.Message):
    if check_admin(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
    else:
        m = message.get_full_command()
        values = m[1].split(" ")
        if del_user(values[0], int(values[1])) == True:
            await message.reply("تم الحذف بنجاح")
        else:
            await message.reply("حدث خطأ عند الحذف")

# create photos menu stage
@dp.message_handler(lambda message: message.text == "الصور 📷")
async def pics(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await bot.send_message(message.chat.id, "اختر من الصور", reply_markup=pic_markup)


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


# create add HW command handler
@dp.message_handler(lambda message: message.text == 'اضافة واجب 📝')
async def HW_managment(message: types.Message):
    if get_manager_stage(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
    else:
        await AddHW.day.set()
        await message.reply("اختر اليوم", reply_markup=hw_day_input_markup)

# get the day from the user
@dp.message_handler(state=AddHW.day)
async def process_day(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['day'] = message.text

    await AddHW.next()
    await message.reply("ارسل الواجب", reply_markup=cancel_input_markup)

# get add hw message handler
@dp.message_handler(state=AddHW.hw)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['hw'] = message.text
        try:
            if add_hw(get_manager_stage(message.from_user.id), data['day'], data['hw']) == True:
                await message.reply("تم الاضافة بنجاح", reply_markup=get_user_markup(message.from_user.id))
        except:
            await bot.send_message(message.chat.id, "حدث خطأ ما\nيرجى التحقق من المدخلات أو اذا كان لديك الصلاحيات لتنفيذ الاجراء", reply_markup=get_user_markup(message.from_user.id))
    await state.finish()


# create view hw message handler
@dp.message_handler(lambda message: message.text == "اختيار يوم 📋")
async def select_hw(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await message.reply("يجب اختيار المرحلة اولا!", reply_markup=get_user_markup(message.from_user.id))
    else:
        await Viewhw.day.set()
        await bot.send_message(message.chat.id, "اختر اليوم ", reply_markup=hw_day_input_markup)

@dp.message_handler(state=Viewhw.day)
async def view_by_day(message: types.Message, state=Viewhw):
    async with state.proxy() as data:
        data['day'] = message.text
        if check_user_exist(message.from_user.id) == False:
            await bot.send_message(message.chat.id, "يجب اختيار المرحلة اولا!", reply_markup=get_user_markup(message.from_user.id))
        else:
            try:
                await message.reply(get_hw(check_user_stage(message.from_user.id), data['day']), reply_markup=get_user_markup(message.from_user.id))
            except:
                await message.reply("فشل عرض الواجب!")
    await state.finish()

# create delete HW command handler
@dp.message_handler(lambda message: message.text == 'حذف واجب 📝')
async def HW_managment(message: types.Message):
    if get_manager_stage(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
    else:
        await DelHW.day.set()
        await message.reply("اختر اليوم", reply_markup=hw_day_input_markup)

# get the day from the user
@dp.message_handler(state=DelHW.day)
async def process_day(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['day'] = message.text
        stage = get_manager_stage(message.from_user.id)
        if add_hw(stage, data['day'], "لا شيء") == True:
            await message.reply("تم حذف الواجب", reply_markup=get_user_markup(message.from_user.id))
        else:
            await bot.send_message(message.chat.id, "فشل حذف الواجب", reply_markup=get_user_markup(message.from_user.id))
    await state.finish()

# create add manager command handler
@dp.message_handler(lambda message: message.text == 'اضافة مشرف 💂')
async def user_managment(message: types.Message):
    if check_admin(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
    else:
        await AddManager.stage.set()
        await message.reply("اختر المرحلة", reply_markup=add_del_man_stage_input_markup)

# get the stage from the user
@dp.message_handler(state=AddManager.stage)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['stage'] = message.text

    await AddManager.next()
    await message.reply("ارسل الID الخاص بالمستخدم", reply_markup=cancel_input_markup)

# get user id form the user and end data entry
@dp.message_handler(lambda message: message.text.isdigit(), state=AddManager.uid)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['uid'] = int(message.text)
        if add_manager(data['stage'], data['uid']) == True:
            await message.reply("تم الاضافة بنجاح", reply_markup=get_user_markup(message.from_user.id))
        else:
            await bot.send_message(message.chat.id, "فشل اضافة المشرف", reply_markup=get_user_markup(message.from_user.id))
    await state.finish()



# create delete manager command handler
@dp.message_handler(lambda message: message.text == 'حذف مشرف 💂')
async def user_managment(message: types.Message):
    if check_admin(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
    else:
        await DelManager.stage.set()
        await message.reply("اختر المرحلة", reply_markup=add_del_man_stage_input_markup)

# get the stage from the user
@dp.message_handler(state=DelManager.stage)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['stage'] = message.text

    await DelManager.next()
    await message.reply("ارسل الID الخاص بالمستخدم", reply_markup=cancel_input_markup)

# get user id form the user and end data entry
@dp.message_handler(lambda message: message.text.isdigit(), state=DelManager.uid)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['uid'] = int(message.text)
        if del_manager(data['stage'], data['uid']) == True:
            await message.reply("تم الحذف بنجاح", reply_markup=get_user_markup(message.from_user.id))
        else:
            await bot.send_message(message.chat.id, "فشل حذف المشرف", reply_markup=get_user_markup(message.from_user.id))
    await state.finish()

# send announcement for a stage by manager
@dp.message_handler(lambda message: message.text == 'أرسال اعلان 📢')
async def anno_managment(message: types.Message):
    if get_manager_stage(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
    else:
        await Anno.m.set()
        await message.reply("ارسل الرسالة التي تريد اعلانها", reply_markup=cancel_input_markup)

# get the message from the manager and send it to the student
@dp.message_handler(state=Anno.m)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['m'] = f"أعلان  📢 بواسطة: @{message.from_user.username}\n\n"
        data['m'] += message.text
        try:
            for user in get_users_uid(message.from_user.id):
                await bot.send_message(user, data['m'])
            await message.reply("تم ارسال الاعلان بنجاح", reply_markup=get_user_markup(message.from_user.id))
        except:
            await message.reply("فشل ارسال الاعلان", reply_markup=get_user_markup(message.from_user.id))
    await state.finish()

# send announcement for all stages by admin
@dp.message_handler(lambda message: message.text == 'أرسال اعلان للجميع 📢')
async def anno_managment(message: types.Message):
    if check_admin(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
    else:
        await AnnoAll.m.set()
        await message.reply("ارسل الرسالى التي تريد اعلانها", reply_markup=cancel_input_markup)

# get the message from the manager and send it to the student
@dp.message_handler(state=AnnoAll.m)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['m'] = f"أعلان للجميع 📢 بواسطة: @{message.from_user.username}\n\n"
        data['m'] += message.text
        try:
            for user in get_users_uid_all(message.from_user.id):
                await bot.send_message(user, data['m'])
            await message.reply("تم ارسال الاعلان بنجاح", reply_markup=get_user_markup(message.from_user.id))
        except:
            await message.reply("فشل ارسال الاعلان", reply_markup=get_user_markup(message.from_user.id))
    await state.finish()

# create list of user id and username for all users 
@dp.message_handler(lambda message: message.text == "عرض جميع المستخدمين 📋")
async def make_list(message: types.Message):
    if check_admin(message.from_user.id) != True:
        await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
    else:
        uids = get_users_uid_all(message.from_user.id)
        usernames = get_all_users_username()
        message_text = ""
        for (uid, username) in zip(uids, usernames):
            message_text += f"أيدي المستخدم {uid}   يوزر المستخدم @{username}\n"
        await message.reply(message_text, reply_markup=get_user_markup(message.from_user.id))

# create admin permissions list getter 
@dp.message_handler(lambda message: message.text == "عرض صلاحيات الادمن 👮")
async def view_admin_permissions(message: types.Message):
    if check_admin(message.from_user.id) == True:
        await message.reply("تم عرض صلاحيات الادمن", reply_markup=admin_markup())
    else:
        await message.reply("ليس لديك الصلاحية لعرض هذه القائمة", reply_markup=get_user_markup(message.from_user.id))


# create manager premissions list getter 
@dp.message_handler(lambda message: message.text == "عرض صلاحيات المشرف 💂")
async def view_man_permissions(message: types.Message):
    if get_manager_stage(message.from_user.id) != False:
        await message.reply("تم عرض صلاحيات المشرف", reply_markup=manager_markup())
    else:
        await message.reply("ليس لديك الصلاحية لعرض هذه القائمة", reply_markup=get_user_markup(message.from_user.id))

# create merge pdfs message handler
# ask the user about the file name
@dp.message_handler(lambda message: message.text == "دمج ملفات pdf")
async def merge(message: types.Message, state: FSMContext):
    if check_user_exist(message.from_user.id) == False:
        await message.reply("اختر المرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
    else:
        await MergePdf.folder.set()
        randfile = ''.join(random.choice(string.ascii_lowercase) for i in range(20))
        os.system(f"mkdir cache/{randfile}")
        async with state.proxy() as data:
            data['folder'] = f"cache/{randfile}"
        await MergePdf.next()
        await message.reply("ماذا تريد ان تسمي الملف؟", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add("الغاء الدمج"))

# get the file name
@dp.message_handler(state=MergePdf.file_name)
async def get_file_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['file_name'] = message.text

    await MergePdf.next()
    await bot.send_message(message.chat.id, "ارسل الملفات وعند الرد على جميع الملفات برسالة 'تم تنزيل الملف' يمكنك ارسل أو ضعط دمج", reply_markup=merge_markup)


# create merge pdfs message handler
@dp.message_handler(lambda message: message.text == "الغاء الدمج", state=MergePdf)
async def merge(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        os.system(f"rm -rf {data['folder']}")
        await message.reply("تم الغاء الدمج وحذف الملفات", reply_markup=get_user_markup(message.from_user.id))
    await state.finish()

# create pdfs getter
@dp.message_handler(state=MergePdf.temp, content_types=ContentTypes.DOCUMENT)
async def pdf_getter(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if document := message.document:
            await document.download(
                destination_file=f"{data['folder']}/{document.file_name}",
            )
            await message.reply("تم تنزيل الملف")
            with open((data['folder']+"/files"), 'a+') as fls:
                fls.write(f"{data['folder']}/{document.file_name};")
                fls.close()

# create merge pdf command handler
@dp.message_handler(lambda message: message.text == "دمج" ,state=MergePdf.temp)
async def merge_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        f = open((data['folder'] + "/files"), 'r')
        file = f.read()
        pdfs = file.split(";")
        pdfs.remove('')
        try:
            await bot.send_document(message.chat.id, document=open(merge_pdfs(pdfs, data['folder'], data['file_name']), 'rb'), reply_markup=get_user_markup(message.from_user.id))
        except:
            await message.reply("فشل دمج الملفات")
            os.system(f"rm -rf {data['folder']}")
        os.system(f"rm -rf {data['folder']}")
    await state.finish()

# create images to pdf message handler
# ask the user about the name of the file
@dp.message_handler(lambda message: message.text == "تحويل الصور الى pdf")
async def merge(message: types.Message, state: FSMContext):
    if check_user_exist(message.from_user.id) == False:
        await message.reply("اختر المرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
    else:
        await MergeImages.folder.set()
        randfile = ''.join(random.choice(string.ascii_lowercase) for i in range(20))
        os.system(f"mkdir cache/{randfile}")
        async with state.proxy() as data:
            data['folder'] = f"cache/{randfile}"
        await MergeImages.next()
        await message.reply("ماذا تريد ان تسمي الملف؟", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add("الغاء الدمج"))


# get the images from the user
@dp.message_handler(state=MergeImages.file_name)
async def merge(message: types.Message, state: FSMContext):
    if check_user_exist(message.from_user.id) == False:
        await message.reply("اختر المرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
    else:
        async with state.proxy() as data:
            data['file_name'] = message.text

        await MergeImages.next()
        await message.reply("ارسل الصور وعند الرد على جميع الصور برسالة 'تم تنزيل الملف' يمكنك ارسل أو ضعط دمج", reply_markup=merge_markup)

# create cancel images merge to pdf message handler
@dp.message_handler(lambda message: message.text == "الغاء الدمج", state=MergeImages)
async def merge(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        os.system(f"rm -rf {data['folder']}")
        await message.reply("تم الغاء الدمج وحذف الملفات", reply_markup=get_user_markup(message.from_user.id))
    await state.finish()

# create pdfs getter
@dp.message_handler(state=MergeImages.temp, content_types=ContentTypes.DOCUMENT)
async def pdf_getter(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if document := message.document:
            await document.download(
                destination_file=f"{data['folder']}/{document.file_name}",
            )
            await message.reply("تم تنزيل الملف")
            with open((data['folder']+"/files"), 'a+') as fls:
                fls.write(f"{data['folder']}/{document.file_name};")
                fls.close()

# create merge pdf command handler
@dp.message_handler(lambda message: message.text == "دمج" ,state=MergeImages.temp)
async def merge(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        f = open((data['folder'] + "/files"), 'r')
        file = f.read()
        pdfs = file.split(";")
        pdfs.remove('')
        try:
            await bot.send_message(message.chat.id, "جاري دمج الصور و رفع الملف")
            await bot.send_document(message.chat.id, document=open(images_to_pdf(pdfs, data['folder'], data['file_name']), 'rb'), reply_markup=get_user_markup(message.from_user.id))
        except:
            await message.reply("فشل دمج الملفات")
        os.system(f"rm -rf {data['folder']}")
    await state.finish()
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
async def uknow_messages(message: types.Message):
    await message.reply("""
عذرا لم افهم ماذا تقول
يمكنك ارسال بدء لعرض الاوامر أو اضغط على
/start
""")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)