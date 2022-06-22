import asyncio
from aiogram import types
from cmds.classes import Viewhw
from cmds.markup_manager import get_user_markup, custom_markup
from cmds.hw_getter import get_hw, get_hw_allweek
from cmds import user_manager

async def View_hw_select_day(message, bot):
	if user_manager.check_user_exist(message.from_user.id) == False:
	    await message.reply("يجب اختيار المرحلة اولا!", reply_markup=get_user_markup(message.from_user.id))
	else:
	    await Viewhw.day.set()
	    await bot.send_message(message.chat.id, "اختر اليوم ", reply_markup=custom_markup(["الاحد","الاثنين","الثلاثاء","الاربعاء","الخميس","الغاء الادخال"]))

async def View_hw_command(message, state, bot):
	async with state.proxy() as data:
	    data['day'] = message.text
	    if user_manager.check_user_exist(message.from_user.id) == False:
	        await bot.send_message(message.chat.id, "يجب اختيار المرحلة اولا!", reply_markup=get_user_markup(message.from_user.id))
	    else:
	        try:
	            await message.reply(get_hw(user_manager.check_user_stage(message.from_user.id), data['day']), reply_markup=get_user_markup(message.from_user.id))
	        except:
	            await message.reply("فشل عرض الواجب!")
	await state.finish()

async def View_hw_all_command(message, bot):
	if user_manager.check_user_exist(message.from_user.id) == False:
	    await bot.send_message(message.chat.id, "انت غير مسجل!\nاختر المرحلة اولا", reply_markup=new_user_main_markup)
	else:
	    stage = user_manager.check_user_stage(message.from_user.id)
	    if stage == False:
	        await message.reply("انت لا تنتمي الى مرحلة")
	    else:
	        await message.reply(get_hw_allweek(stage))