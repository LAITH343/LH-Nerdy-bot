import asyncio
from aiogram import types
from cmds.classes import Selcet_Stage
from cmds.user_manager import check_user_exist, add_user
from cmds.markup_manager import get_user_markup, custom_markup
from cmds import error_reporter

async def Select_stage(message, bot):
	try:
		if check_user_exist(message.from_user.id) == False:
			await Selcet_Stage.stage.set()
			await message.answer("أختر المرحلة", reply_markup=custom_markup(["مرحلة اولى","مرحلة ثانية","مرحلة ثالثة","مرحلة رابعة"]))
	except Exception as e:
		await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
		await error_reporter.report(message, bot, "Select_stage", e)

async def Add_user(message, state, bot):
	try:
		if check_user_exist(message.from_user.id) == False:
			stage_translate = {
				"مرحلة اولى": "stage1",
				"مرحلة ثانية": "stage2",
				"مرحلة ثالثة": "stage3",
				"مرحلة رابعة": "stage4",
			}
			if message.from_user.username != None:
				add_user(stage_translate[message.text], message.from_user.id, message.from_user.full_name, message.from_user.username)
				await message.answer("تم الاضافة", reply_markup=get_user_markup(message.from_user.id))
			else:
				await message.answer("يرجى وضع اسم مستخدم (المعرف) أولا", reply_markup=get_user_markup(message.from_user.id))
			await state.finish()
	except Exception as e:
		await state.finish()
		await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
		await error_reporter.report(message, bot, "Add_user", e)
