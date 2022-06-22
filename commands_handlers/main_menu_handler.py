import asyncio
from aiogram import types
from cmds.markup_manager import manager_markup, admin_markup, get_user_markup
from cmds.user_manager import check_admin, get_manager_stage

async def View_manager_list(message):
	if get_manager_stage(message.from_user.id) != False:
	    await message.reply("تم عرض صلاحيات المشرف", reply_markup=manager_markup())
	else:
	    await message.reply("ليس لديك الصلاحية لعرض هذه القائمة", reply_markup=get_user_markup(message.from_user.id))

async def View_admin_list(message):
	if check_admin(message.from_user.id) == True:
	    await message.reply("تم عرض صلاحيات الادمن", reply_markup=admin_markup())
	else:
	    await message.reply("ليس لديك الصلاحية لعرض هذه القائمة", reply_markup=get_user_markup(message.from_user.id))