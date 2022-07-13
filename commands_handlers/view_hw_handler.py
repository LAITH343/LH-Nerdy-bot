from cmds.classes import Viewhw
from cmds.markup_manager import get_user_markup, custom_markup
from cmds.hw_manager import get_hw, get_hw_allweek
from cmds import user_manager
from cmds import error_reporter
from config import bot


async def View_hw_select_day(message):
	try:
		if not user_manager.check_user_exist(message.from_user.id):
			await message.reply("يجب اختيار المرحلة اولا!", reply_markup=get_user_markup(message.from_user.id))
		else:
			await Viewhw.day.set()
			await bot.send_message(message.chat.id, "اختر اليوم ", reply_markup=custom_markup(["الاحد","الاثنين","الثلاثاء","الاربعاء","الخميس","الغاء الادخال"]))
	except Exception as e:
		await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
		await error_reporter.report(message, bot, "View_hw_select_day", e)


async def View_hw_command(message, state):
	try:
		day_translate = {
			"الاحد": "sunday",
			"الاثنين": "monday",
			"الثلاثاء": "tuesday",
			"الاربعاء": "wednesday",
			"الخميس": "thursday"
		}
		async with state.proxy() as data:
			data['day'] = message.text
			await message.reply(get_hw(user_manager.check_user_stage(message.from_user.id), day_translate[data['day']]), reply_markup=get_user_markup(message.from_user.id))
		await state.finish()
	except Exception as e:
		await state.finish()
		await message.answer("فشل عرض الواجب!", reply_markup=get_user_markup(message.from_user.id))
		await error_reporter.report(message, bot, "View_hw_command", e)


async def View_hw_all_command(message):
	try:
		stage = user_manager.check_user_stage(message.from_user.id)
		await message.reply(get_hw_allweek(stage))
	except Exception as e:
		await message.answer("فشل عرض الواجب!", reply_markup=get_user_markup(message.from_user.id))
		await error_reporter.report(message, bot, "View_hw_all_command", e)


def reg(dp):
	dp.register_message_handler(View_hw_select_day, text="اختيار يوم 📋")
	dp.register_message_handler(View_hw_command, state=Viewhw.day)
	dp.register_message_handler(View_hw_all_command, text="عرض واجبات الاسبوع 📖")
