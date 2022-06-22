import asyncio
from aiogram import types
from cmds.user_manager import get_manager_stage, get_users_uid
from cmds.markup_manager import get_user_markup, custom_markup
from cmds.classes import DelHW, AddHW, Anno
from cmds.hw_adder import add_hw

async def Manager_del_hw(message, bot):
	if get_manager_stage(message.from_user.id) == False:
	    await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
	else:
	    await DelHW.day.set()
	    await message.reply("اختر اليوم", reply_markup=custom_markup(["الاحد","الاثنين","الثلاثاء","الاربعاء","الخميس","الغاء الادخال"]))# hw_day_input_markup

async def Manager_del_hw_command(message, state, bot):
	async with state.proxy() as data:
	    data['day'] = message.text
	    stage = get_manager_stage(message.from_user.id)
	    if add_hw(stage, data['day'], "لا شيء") == True:
	        await message.reply("تم حذف الواجب", reply_markup=get_user_markup(message.from_user.id))
	    else:
	        await bot.send_message(message.chat.id, "فشل حذف الواجب", reply_markup=get_user_markup(message.from_user.id))
	await state.finish()

async def Manager_add_hw(message, bot):
	if get_manager_stage(message.from_user.id) == False:
	    await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
	else:
	    await AddHW.day.set()
	    await message.reply("اختر اليوم", reply_markup=custom_markup(["الاحد","الاثنين","الثلاثاء","الاربعاء","الخميس","الغاء الادخال"]))

async def Manager_get_day(message, state):
	async with state.proxy() as data:
	    data['day'] = message.text

	await AddHW.next()
	await message.reply("ارسل الواجب", reply_markup=custom_markup(["الغاء الادخال"]))# cancel_input_markup

async def Manager_add_hw_command(message, state, bot):
	async with state.proxy() as data:
	    data['hw'] = message.text
	    try:
	        if add_hw(get_manager_stage(message.from_user.id), data['day'], data['hw']) == True:
	            await message.reply("تم الاضافة بنجاح", reply_markup=get_user_markup(message.from_user.id))
	    except:
	        await bot.send_message(message.chat.id, "حدث خطأ ما\nيرجى التحقق من المدخلات أو اذا كان لديك الصلاحيات لتنفيذ الاجراء", reply_markup=get_user_markup(message.from_user.id))
	await state.finish()

async def Manager_send_anno(message, bot):
	if get_manager_stage(message.from_user.id) == False:
	    await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
	else:
	    await Anno.m.set()
	    await message.reply("ارسل الرسالة التي تريد اعلانها", reply_markup=custom_markup(["الغاء الادخال"]))

async def Manager_send_anno_command(message, state, bot):
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