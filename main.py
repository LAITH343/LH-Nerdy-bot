import logging
from aiogram import Bot, Dispatcher, executor, types
from cmds.user_check import check, check_user_exist
from s import answer
from pdfs_links import links
from cmds.myinfo import myInfo
from hw_adder import add_hw
from hw_getter import get_hw, get_hw_allweek
from cmds.check_user_stage import check_stage
from add_user import add_user
from del_user import del_user

API_TOKEN = '1294672480:AAGzpGRBS1ACOkeRftg_a_rTrFFiJTTsmo8'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# create main menu 
main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
main_markup.add("عرض الواجبات")
main_markup.add("ملازم")
main_markup.add("الجداول")
main_markup.add("الصور")
main_markup.add("معلوماتي")
main_markup.add("أغلاق")

# create main menu 
new_user_main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
new_user_main_markup.add("اختيار المرحلة")
new_user_main_markup.add("أغلاق")

# create pdf menu 
pdf_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
pdf_markup.add("منطق رقمي")
pdf_markup.add("برمجة سي بلس بلس 2")
pdf_markup.add("اساسيات البرمجة")
pdf_markup.add("الرجوع للقائمة الرئيسية")

# create s exams menu 
s_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
s_markup.add("جدول المرحلة الاولى")
s_markup.add("جدول المرحلة الثانية")
s_markup.add("جدول المرحلة الثالثة")
s_markup.add("جدول المرحلة الرابعة")
s_markup.add("الرجوع للقائمة الرئيسية")

# create hw menu 
hw_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
hw_markup.add("عرض واجبات يوم الاحد")
hw_markup.add("عرض واجبات يوم الاثنين")
hw_markup.add("عرض واجبات يوم الثلاثاء")
hw_markup.add("عرض واجبات يوم الاربعاء")
hw_markup.add("عرض واجبات يوم الخميس")
hw_markup.add("عرض واجبات الاسبوع")
hw_markup.add("الرجوع للقائمة الرئيسية")

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
pic_markup.add("الرجوع للقائمة الرئيسية")

# set new user stage
@dp.message_handler(lambda message: message.text == "مرحلة اولى")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "لا يمكنك الاختيار أنت مسجل مسبقا", reply_markup=main_markup)
    else:
        if add_user("stage1", message.from_user.id) == True:
            await bot.send_message(message.chat.id, "تم الاظافة", reply_markup=main_markup)
        else:
            await bot.send_message(message.chat.id, "فشل الاضافة", reply_markup=stages_markup)

@dp.message_handler(lambda message: message.text == "مرحلة ثانية")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "لا يمكنك الاختيار أنت مسجل مسبقا", reply_markup=main_markup)
    else:
        if add_user("stage2", message.from_user.id) == True:
            await bot.send_message(message.chat.id, "تم الاظافة", reply_markup=main_markup)
        else:
            await bot.send_message(message.chat.id, "فشل الاضافة", reply_markup=stages_markup)

@dp.message_handler(lambda message: message.text == "مرحلة ثالثة")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "لا يمكنك الاختيار أنت مسجل مسبقا", reply_markup=main_markup)
    else:
        if add_user("stage3", message.from_user.id) == True:
            await bot.send_message(message.chat.id, "تم الاظافة", reply_markup=main_markup)
        else:
            await bot.send_message(message.chat.id, "فشل الاضافة", reply_markup=stages_markup)

@dp.message_handler(lambda message: message.text == "مرحلة رابعة")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "لا يمكنك الاختيار أنت مسجل مسبقا", reply_markup=main_markup)
    else:
        if add_user("stage4", message.from_user.id) == True:
            await bot.send_message(message.chat.id, "تم الاظافة", reply_markup=main_markup)
        else:
            await bot.send_message(message.chat.id, "فشل الاضافة", reply_markup=stages_markup)
    

@dp.message_handler(lambda message: message.text == "اختيار المرحلة")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "لا يمكنك الاختيار أنت مسجل مسبقا", reply_markup=main_markup)
    else:
        await bot.send_message(message.chat.id, "اختر المرحلة\nملاحظة مهمة: يمكنك اختيار المرحلة لمرة واحدة فقط", reply_markup=stages_markup)


# create start message/command handler
@dp.message_handler(lambda message: message.text in ["start", "بدء", "/start"])
async def send_welcome(message: types.Message):
    if check_user_exist(message.from_user.id) == True:
        await bot.send_message(message.chat.id, "أهلا بك في البوت", reply_markup=main_markup)
    else:
        await bot.send_message(message.chat.id, "أهلا بك\nاختر المرحلة", reply_markup=new_user_main_markup)

# create pdf menu 
@dp.message_handler(lambda message: message.text == "ملازم")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await bot.send_message(message.chat.id, "اختر الملف من القائمة", reply_markup=pdf_markup)

#create my info message
@dp.message_handler(lambda message: message.text == "معلوماتي")
async def echo(message: types.Message):
    await message.reply(myInfo(message))

# create exit message handler
@dp.message_handler(lambda message: message.text == "أغلاق")
async def echo(message: types.Message):
    cmarkup = types.ReplyKeyboardRemove()
    await message.reply("تم", reply_markup=cmarkup)

# create collage logo message handler
@dp.message_handler(lambda message: message.text == "شعار الكلية")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("جاري رفع الصورة... يرجى الانتظار")
        await bot.send_photo(message.chat.id, types.InputFile.from_url('https://duc.edu.iq/wp-content/uploads/2020/04/unnamed-file-1.png'))

# create cs department logo message handler
@dp.message_handler(lambda message: message.text == "شعار القسم")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("جاري رفع الصورة... يرجى الانتظار")
        await bot.send_photo(message.chat.id, types.InputFile.from_url('https://api.portal.duc.edu.iq/uploads/view/1645104654002.png'))

# create s exams menu 
@dp.message_handler(lambda message: message.text == "جدول الامتحانات")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await bot.send_message(message.chat.id, "يمكنك الاختيار لعرض الجدول", reply_markup=s_markup)

# create first stage s exams message handler 
@dp.message_handler(lambda message: message.text == "جدول المرحلة الاولى")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply(answer("جدول المرحلة الاولى"))

# create second stage s exams message handler 
@dp.message_handler(lambda message: message.text == "جدول المرحلة الثانية")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply(answer("جدول المرحلة الثانية"))


# create third stage s exams message handler 
@dp.message_handler(lambda message: message.text == "جدول المرحلة الثالثة")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply(answer("جدول المرحلة الثالثة"))


# create fourth stage s exams message handler 
@dp.message_handler(lambda message: message.text == "جدول المرحلة الرابعة")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply(answer("جدول المرحلة الرابعة"))

# create back to main menu message handler
@dp.message_handler(lambda message: message.text == "الرجوع للقائمة الرئيسية")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("تم الرجوع الى القائمة الرئيسية", reply_markup=main_markup)

# create logic pdf message handler
@dp.message_handler(lambda message: message.text == "منطق رقمي")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("جاري الرفع... ")
        await bot.send_document(message.chat.id, links("logic"))

# create c++ pdf message handler
@dp.message_handler(lambda message: message.text == "برمجة سي بلس بلس 2")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("جاري الرفع... ")
        await bot.send_document(message.chat.id, links("cplusplus"))

# create pf pdf message handler
@dp.message_handler(lambda message: message.text == "اساسيات البرمجة")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await message.reply("جاري الرفع... ")
        await bot.send_document(message.chat.id, links("pf"))

# create hw adder 
@dp.message_handler(commands='addhw')
async def set_hw(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        m = message.get_full_command()
        values = m[1].split(" ")
        if add_hw(values[0], values[1], values[2]) == True:
            await message.reply("تم الاظافة بنجاح")
        else:
            await message.reply("حدث خطأ عند الادخال")


# create hw messages menu 
@dp.message_handler(lambda message: message.text == "عرض الواجبات")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await bot.send_message(message.chat.id, "اختر اليوم من القائمة", reply_markup=hw_markup)


# create hw sunday message handler
@dp.message_handler(lambda message: message.text == "عرض واجبات يوم الاحد")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        stage = check_stage(message.from_user.id)
        if stage == False:
            await message.reply("انت لا تنتمي الى مرحلة")
        else:
            await message.reply(get_hw(stage, "الاحد"))

# create hw monday message handler
@dp.message_handler(lambda message: message.text == "عرض واجبات يوم الاثنين")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        stage = check_stage(message.from_user.id)
        if stage == False:
            await message.reply("انت لا تنتمي الى مرحلة")
        else:
            await message.reply(get_hw(stage, "الاثنين"))

# create hw tuesday message handler
@dp.message_handler(lambda message: message.text == "عرض واجبات يوم الثلاثاء")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        stage = check_stage(message.from_user.id)
        if stage == False:
            await message.reply("انت لا تنتمي الى مرحلة")
        else:
            await message.reply(get_hw(stage, "الثلاثاء"))

# create hw wednesday message handler
@dp.message_handler(lambda message: message.text == "عرض واجبات يوم الاربعاء")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        stage = check_stage(message.from_user.id)
        if stage == False:
            await message.reply("انت لا تنتمي الى مرحلة")
        else:
            await message.reply(get_hw(stage, "الاربعاء"))

# create hw thursday message handler
@dp.message_handler(lambda message: message.text == "عرض واجبات يوم الخميس")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        stage = check_stage(message.from_user.id)
        if stage == False:
            await message.reply("انت لا تنتمي الى مرحلة")
        else:
            await message.reply(get_hw(stage, "الخميس"))

# create hw all week message handler
@dp.message_handler(lambda message: message.text == "عرض واجبات الاسبوع")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        stage = check_stage(message.from_user.id)
        if stage == False:
            await message.reply("انت لا تنتمي الى مرحلة")
        else:
            await message.reply(get_hw_allweek(stage))

# create delete user command handler
@dp.message_handler(commands='deluser')
async def set_hw(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        m = message.get_full_command()
        values = m[1].split(" ")
        if del_user(values[0], int(values[1])) == True:
            await message.reply("تم الحذف بنجاح")
        else:
            await message.reply("حدث خطأ عند الحذف")

# create photos menu stage
@dp.message_handler(lambda message: message.text == "الصور")
async def echo(message: types.Message):
    if check_user_exist(message.from_user.id) == False:
        await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
    else:
        await bot.send_message(message.chat.id, "اختر من الصور", reply_markup=pic_markup)


# create unkown message handler
@dp.message_handler()
async def echo(message: types.Message):
    await message.reply("""
عذرا لم افهم ماذا تقول
يمكنك ارسال بدء لعرض الاوامر أو اضغط على
/start
""")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)