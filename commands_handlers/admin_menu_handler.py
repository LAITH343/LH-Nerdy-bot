import asyncio
from aiogram import types
from cmds.user_manager import get_all_usernames, check_admin, del_manager, add_manager, get_users_uid
from cmds.markup_manager import get_user_markup, custom_markup
from cmds.classes import AnnoAll, AddManager, DelManager

async def create_users_list():
	message_list = ""
	uid = get_users_uid()
	username = get_all_usernames()
	for i in range(len(get_all_usernames())):
			message_list +=f"أي دي المستخدم {uid[i]} يوزر المستخدم @{username[i]}\n"
	return message_list

async def View_all_users(message, bot):
	if check_admin(message.from_user.id) != True:
	    await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
	else:
		message_text = await create_users_list()
		await message.answer(message_text, reply_markup=get_user_markup(message.from_user.id))

async def Send_anno_4all(message, bot):
	if check_admin(message.from_user.id) == False:
	    await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
	else:
	    await AnnoAll.m.set()
	    await message.reply("ارسل الرسالى التي تريد اعلانها", reply_markup=custom_markup(["الغاء الادخال"])) #cancel_input_markup

async def Get_anno_msg_and_send(message, state, bot):
	async with state.proxy() as data:
	    data['m'] = f"أعلان للجميع 📢 بواسطة: @{message.from_user.username}\n\n"
	    data['m'] += message.text
	    try:
	        for user in get_users_uid():
	            await bot.send_message(user, data['m'])
	        await message.reply("تم ارسال الاعلان بنجاح", reply_markup=get_user_markup(message.from_user.id))
	    except:
	        await message.reply("فشل ارسال الاعلان", reply_markup=get_user_markup(message.from_user.id))
	await state.finish()

async def Delete_manager(message, bot):
	if check_admin(message.from_user.id) == False:
	    await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
	else:
	    await DelManager.stage.set()
	    await message.reply("اختر المرحلة", reply_markup=custom_markup(["stage1","stage2","stage3","stage4","الغاء الادخال"]))

async def Delete_manager_get_stage(message, state):
	async with state.proxy() as data:
	    data['stage'] = message.text

	await DelManager.next()
	await message.reply("ارسل الID الخاص بالمستخدم", reply_markup=custom_markup(["الغاء الادخال"]))

async def Delete_manager_get_uid_and_del(message, state, bot):
	async with state.proxy() as data:
	    data['uid'] = int(message.text)
	    if del_manager(data['uid']) == True:
	        await message.reply("تم الحذف بنجاح", reply_markup=get_user_markup(message.from_user.id))
	    else:
	        await bot.send_message(message.chat.id, "فشل حذف المشرف", reply_markup=get_user_markup(message.from_user.id))
	await state.finish()

async def Add_manager(message, bot):
	if check_admin(message.from_user.id) == False:
	    await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
	else:
	    await AddManager.stage.set()
	    await message.reply("اختر المرحلة", reply_markup=custom_markup(["stage1","stage2","stage3","stage4","الغاء الادخال"])) # add_del_man_stage_input_markup

async def Add_manager_get_stage(message, state):
	async with state.proxy() as data:
	    data['stage'] = message.text

	await AddManager.next()
	await message.reply("ارسل الID الخاص بالمستخدم", reply_markup=custom_markup(["الغاء الادخال"]))

async def Add_manager_get_uid_and_add(message, state, bot):
	async with state.proxy() as data:
	    data['uid'] = int(message.text)
	    if add_manager(data['uid']) == True:
	        await message.reply("تم الاضافة بنجاح", reply_markup=get_user_markup(message.from_user.id))
	    else:
	        await bot.send_message(message.chat.id, "فشل اضافة المشرف", reply_markup=get_user_markup(message.from_user.id))
	await state.finish()
