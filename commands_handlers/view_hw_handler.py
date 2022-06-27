from cmds.classes import Viewhw
from cmds.markup_manager import get_user_markup, custom_markup
from cmds.hw_getter import get_hw, get_hw_allweek
from cmds import user_manager
from cmds import error_reporter


async def View_hw_select_day(message, bot):
	try:
		if not user_manager.check_user_exist(message.from_user.id):
			await message.reply("يجب اختيار المرحلة اولا!", reply_markup=get_user_markup(message.from_user.id))
		else:
			await Viewhw.day.set()
			await bot.send_message(message.chat.id, "اختر اليوم ", reply_markup=custom_markup(["الاحد","الاثنين","الثلاثاء","الاربعاء","الخميس","الغاء الادخال"]))
	except Exception as e:
		await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
		await error_reporter.report(message, bot, "View_hw_select_day", e)


async def View_hw_command(message, state, bot):
	try:
		async with state.proxy() as data:
			data['day'] = message.text
			if not user_manager.check_user_exist(message.from_user.id):
				await bot.send_message(message.chat.id, "يجب اختيار المرحلة اولا!", reply_markup=get_user_markup(message.from_user.id))
			else:
				await message.reply(get_hw(user_manager.check_user_stage(message.from_user.id), data['day']), reply_markup=get_user_markup(message.from_user.id))
		await state.finish()
	except Exception as e:
		await state.finish()
		await message.answer("فشل عرض الواجب!", reply_markup=get_user_markup(message.from_user.id))
		await error_reporter.report(message, bot, "View_hw_command", e)


async def View_hw_all_command(message, bot):
	try:
		if not user_manager.check_user_exist(message.from_user.id):
			await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
		else:
			stage = user_manager.check_user_stage(message.from_user.id)
			if not stage:
				await message.reply("انت لا تنتمي الى مرحلة")
			else:
				await message.reply(get_hw_allweek(stage))
	except Exception as e:
		await message.answer("فشل عرض الواجب!", reply_markup=get_user_markup(message.from_user.id))
		await error_reporter.report(message, bot, "View_hw_all_command", e)