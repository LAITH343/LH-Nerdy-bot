import logging
from aiogram import Bot, Dispatcher, executor, types
from cmds.user_check import check
from s import answer
from pdfs_links import links
from cmds.myinfo import myInfo

API_TOKEN = '1294672480:AAGzpGRBS1ACOkeRftg_a_rTrFFiJTTsmo8'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# create main menu 
main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
main_markup.add("بدء", "شعار الكلية")
main_markup.add("شعار القسم", "معلوماتي")
main_markup.add("جدول الامتحانات")
main_markup.add("ملازم")
main_markup.add("أغلاق")

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

# create start message/command handler
@dp.message_handler(lambda message: message.text in ["start", "بدء", "/start"])
async def send_welcome(message: types.Message):
    await bot.send_message(message.chat.id, "مرحبا بك في البوت\nيمكنك اختيار من الاوامر", reply_markup=main_markup)

# create pdf menu 
@dp.message_handler(lambda message: message.text == "ملازم")
async def echo(message: types.Message):
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
    await message.reply("جاري رفع الصورة... يرجى الانتظار")
    await bot.send_photo(message.chat.id, types.InputFile.from_url('https://duc.edu.iq/wp-content/uploads/2020/04/unnamed-file-1.png'))

# create cs department logo message handler
@dp.message_handler(lambda message: message.text == "شعار القسم")
async def echo(message: types.Message):
    await message.reply("جاري رفع الصورة... يرجى الانتظار")
    await bot.send_photo(message.chat.id, types.InputFile.from_url('https://api.portal.duc.edu.iq/uploads/view/1645104654002.png'))

# create s exams menu 
@dp.message_handler(lambda message: message.text == "جدول الامتحانات")
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, "يمكنك الاختيار لعرض الجدول", reply_markup=s_markup)

# create first stage s exams message handler 
@dp.message_handler(lambda message: message.text == "جدول المرحلة الاولى")
async def echo(message: types.Message):
    await message.reply(answer("جدول المرحلة الاولى"))

# create second stage s exams message handler 
@dp.message_handler(lambda message: message.text == "جدول المرحلة الثانية")
async def echo(message: types.Message):
    await message.reply(answer("جدول المرحلة الثانية"))


# create third stage s exams message handler 
@dp.message_handler(lambda message: message.text == "جدول المرحلة الثالثة")
async def echo(message: types.Message):
    await message.reply(answer("جدول المرحلة الثالثة"))


# create fourth stage s exams message handler 
@dp.message_handler(lambda message: message.text == "جدول المرحلة الرابعة")
async def echo(message: types.Message):
    await message.reply(answer("جدول المرحلة الرابعة"))

# create back to main menu message handler
@dp.message_handler(lambda message: message.text == "الرجوع للقائمة الرئيسية")
async def echo(message: types.Message):
    await message.reply("تم الرجوع الى القائمة الرئيسية", reply_markup=main_markup)

# create logic pdf message handler
@dp.message_handler(lambda message: message.text == "منطق رقمي")
async def echo(message: types.Message):
    await message.reply("جاري الرفع... ")
    await bot.send_document(message.chat.id, links("logic"))

# create c++ pdf message handler
@dp.message_handler(lambda message: message.text == "برمجة سي بلس بلس 2")
async def echo(message: types.Message):
    await message.reply("جاري الرفع... ")
    await bot.send_document(message.chat.id, links("cplusplus"))

# create pf pdf message handler
@dp.message_handler(lambda message: message.text == "اساسيات البرمجة")
async def echo(message: types.Message):
    await message.reply("جاري الرفع... ")
    await bot.send_document(message.chat.id, links("pf"))

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