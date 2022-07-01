from cmds.logger import send_log
from cmds.user_manager import get_all_usernames, check_admin, del_manager, add_manager, get_users_uid, get_user_username
from cmds.markup_manager import get_user_markup, custom_markup
from cmds.classes import AnnoAll, AddManager, DelManager
from cmds import error_reporter
from config import bot


async def View_all_users(message):
    try:
        if not check_admin(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            for user in await get_all_usernames():
                await message.answer(user, reply_markup=get_user_markup(message.from_user.id))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "View_all_users", e)


async def Send_anno_4all(message):
    try:
        if not check_admin(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await AnnoAll.m.set()
            await message.reply("ارسل الرساله التي تريد اعلانها", reply_markup=custom_markup(["الغاء الادخال"])) #cancel_input_markup
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Send_anno_4all", e)


async def Get_anno_msg_and_send(message, state):
    try:
        async with state.proxy() as data:
            data['m'] = f"أعلان للجميع 📢 بواسطة: @{message.from_user.username}\n\n"
            data['m'] += message.text
            for user in get_users_uid():
                await bot.send_message(user, data['m'])
            await message.reply("تم ارسال الاعلان بنجاح", reply_markup=get_user_markup(message.from_user.id))
            await send_log(message, bot, "ارسال اعلان للجميع", f"تم ارسال\n{data['m']}")
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("فشل ارسال الاعلان", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Get_anno_msg_and_send", e)


async def Delete_manager(message):
    try:
        if not check_admin(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await DelManager.stage.set()
            await message.reply("اختر المرحلة", reply_markup=custom_markup(["مرحلة اولى","مرحلة ثانية","مرحلة ثالثة","مرحلة رابعة","الغاء الادخال"]))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Delete_manager", e)


async def Delete_manager_get_stage(message, state):
    try:
        stage_translate = {
            "مرحلة اولى": "stage1",
            "مرحلة ثانية": "stage2",
            "مرحلة ثالثة": "stage3",
            "مرحلة رابعة": "stage4"
        }
        async with state.proxy() as data:
            data['stage'] = stage_translate[message.text]

        await DelManager.next()
        await message.reply("ارسل الID الخاص بالمستخدم", reply_markup=custom_markup(["الغاء الادخال"]))
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Delete_manager_get_stage", e)


async def Delete_manager_get_uid_and_del(message, state):
    try:
        if not message.text.isdigit():
            await message.answer("يرجى ارسال ارقام فقط")
        else:
            translate = {
                "stage1": "اولى",
                "stage2": "ثانية",
                "stage3": "ثالثة",
                "stage4": "رابعة",
            }
            async with state.proxy() as data:
                data['uid'] = int(message.text)
                del_manager(data['uid'])
                await message.reply("تم الحذف بنجاح", reply_markup=get_user_markup(message.from_user.id))
                await send_log(message, bot, "حذف مشرف", f"تم حذف @{get_user_username(data['uid'])} مشرف مرحلة {translate[data['stage']]}")
            await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("فشل حذف المشرف", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Delete_manager_get_uid_and_del", e)


async def Add_manager(message):
    try:
        if not check_admin(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await AddManager.stage.set()
            await message.reply("اختر المرحلة", reply_markup=custom_markup(["مرحلة اولى","مرحلة ثانية","مرحلة ثالثة","مرحلة رابعة","الغاء الادخال"])) # add_del_man_stage_input_markup
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_manager", e)


async def Add_manager_get_stage(message, state):
    try:
        stage_translate = {
            "مرحلة اولى": "stage1",
            "مرحلة ثانية": "stage2",
            "مرحلة ثالثة": "stage3",
            "مرحلة رابعة": "stage4"
        }
        async with state.proxy() as data:
            data['stage'] = stage_translate[message.text]

        await AddManager.next()
        await message.reply("ارسل الID الخاص بالمستخدم", reply_markup=custom_markup(["الغاء الادخال"]))
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_manager_get_stage", e)


async def Add_manager_get_uid_and_add(message, state):
    try:
        if not message.text.isdigit():
            await message.answer("يرجى ارسال ارقام فقط")
        else:
            translate = {
                "stage1": "اولى",
                "stage2": "ثانية",
                "stage3": "ثالثة",
                "stage4": "رابعة",
            }
            async with state.proxy() as data:
                data['uid'] = int(message.text)
                add_manager(data['uid'])
                await message.reply("تم الاضافة بنجاح", reply_markup=get_user_markup(message.from_user.id))
                await send_log(message, bot, "أضافة مشرف", f"تم أضافة @{get_user_username(data['uid'])} مشرف للمرحلة {translate[data['stage']]}")
            await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("فشل اضافة المشرف", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_manager_get_uid_and_add", e)


def reg(dp):
    dp.register_message_handler(View_all_users, text="عرض جميع المستخدمين 📋")
    dp.register_message_handler(Send_anno_4all, text='أرسال اعلان للجميع 📢')
    dp.register_message_handler(Get_anno_msg_and_send, state=AnnoAll.m)
    dp.register_message_handler(Delete_manager, text ="حذف مشرف 💂")
    dp.register_message_handler(Delete_manager_get_stage, state=DelManager.stage)
    dp.register_message_handler(Delete_manager_get_uid_and_del, state=DelManager.uid)
    dp.register_message_handler(Add_manager, text = "اضافة مشرف 💂")
    dp.register_message_handler(Add_manager_get_stage, state=AddManager.stage)
    dp.register_message_handler(Add_manager_get_uid_and_add, state=AddManager.uid)

