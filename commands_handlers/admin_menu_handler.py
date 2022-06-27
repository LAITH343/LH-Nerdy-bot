from cmds.user_manager import get_all_usernames, check_admin, del_manager, add_manager, get_users_uid
from cmds.markup_manager import get_user_markup, custom_markup
from cmds.classes import AnnoAll, AddManager, DelManager
from cmds import error_reporter


async def View_all_users(message, bot):
    try:
        if not check_admin(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            for user in await get_all_usernames():
                await message.answer(user, reply_markup=get_user_markup(message.from_user.id))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "View_all_users", e)


async def Send_anno_4all(message, bot):
    try:
        if not check_admin(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await AnnoAll.m.set()
            await message.reply("ارسل الرسالى التي تريد اعلانها", reply_markup=custom_markup(["الغاء الادخال"])) #cancel_input_markup
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Send_anno_4all", e)


async def Get_anno_msg_and_send(message, state, bot):
    try:
        async with state.proxy() as data:
            data['m'] = f"أعلان للجميع 📢 بواسطة: @{message.from_user.username}\n\n"
            data['m'] += message.text
            for user in get_users_uid():
                await bot.send_message(user, data['m'])
            await message.reply("تم ارسال الاعلان بنجاح", reply_markup=get_user_markup(message.from_user.id))
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("فشل ارسال الاعلان", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Get_anno_msg_and_send", e)


async def Delete_manager(message, bot):
    try:
        if not check_admin(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await DelManager.stage.set()
            await message.reply("اختر المرحلة", reply_markup=custom_markup(["stage1","stage2","stage3","stage4","الغاء الادخال"]))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Delete_manager", e)


async def Delete_manager_get_stage(message, state, bot):
    try:
        async with state.proxy() as data:
            data['stage'] = message.text

        await DelManager.next()
        await message.reply("ارسل الID الخاص بالمستخدم", reply_markup=custom_markup(["الغاء الادخال"]))
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Delete_manager_get_stage", e)


async def Delete_manager_get_uid_and_del(message, state, bot):
    try:
        async with state.proxy() as data:
            data['uid'] = int(message.text)
            del_manager(data['uid'])
            await message.reply("تم الحذف بنجاح", reply_markup=get_user_markup(message.from_user.id))
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("فشل حذف المشرف", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Delete_manager_get_uid_and_del", e)


async def Add_manager(message, bot):
    try:
        if not check_admin(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await AddManager.stage.set()
            await message.reply("اختر المرحلة", reply_markup=custom_markup(["stage1","stage2","stage3","stage4","الغاء الادخال"])) # add_del_man_stage_input_markup
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_manager", e)


async def Add_manager_get_stage(message, state, bot):
    try:
        async with state.proxy() as data:
            data['stage'] = message.text

        await AddManager.next()
        await message.reply("ارسل الID الخاص بالمستخدم", reply_markup=custom_markup(["الغاء الادخال"]))
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_manager_get_stage", e)


async def Add_manager_get_uid_and_add(message, state, bot):
    try:
        async with state.proxy() as data:
            data['uid'] = int(message.text)
            add_manager(data['uid'])
            await message.reply("تم الاضافة بنجاح", reply_markup=get_user_markup(message.from_user.id))
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("فشل اضافة المشرف", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_manager_get_uid_and_add", e)
