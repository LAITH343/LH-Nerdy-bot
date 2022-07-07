import os

from cmds.logger import send_log
from cmds.statistics import get_bot_users
from cmds.user_manager import get_all_usernames, check_admin, del_manager, add_manager, get_users_uid, \
    get_user_username, change_admin_stage, get_admin_stage
from cmds.markup_manager import get_user_markup, custom_markup, admin_markup
from cmds.classes import AnnoAll, AddManager, DelManager, ChangeStage
from cmds import error_reporter
from config import bot


async def View_all_users(message):
    try:
        if not check_admin(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            file = await get_bot_users()
            await bot.send_document(message.from_user.id, document=open(file, 'rb'))
            os.system(f"rm -f {file}")
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
            await message.reply("تم ارسال الاعلان بنجاح", reply_markup=admin_markup())
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
        if message.text not in ["مرحلة اولى","مرحلة ثانية","مرحلة ثالثة","مرحلة رابعة","الغاء الادخال"]:
            await message.answer("أختر المرحلة أولا")
        else:
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
                await message.reply("تم الحذف بنجاح", reply_markup=admin_markup())
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
        if message.text not in ["مرحلة اولى","مرحلة ثانية","مرحلة ثالثة","مرحلة رابعة","الغاء الادخال"]:
            await message.answer("أختر المرحلة أولا")
        else:
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
                await message.reply("تم الاضافة بنجاح", reply_markup=admin_markup())
                await send_log(message, bot, "أضافة مشرف", f"تم أضافة @{get_user_username(data['uid'])} مشرف للمرحلة {translate[data['stage']]}")
            await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("فشل اضافة المشرف", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_manager_get_uid_and_add", e)


async def change_stage_canceler(message, state):
    try:
        await state.finish()
        await message.answer("تم الغاء التغيير", reply_markup=admin_markup())
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "change_stage_canceler", e)


async def change_stage(message):
    try:
        if not check_admin(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء")
        else:
            stage_translate_revers = {
                "stage1": "مرحلة اولى",
                "stage2": "مرحلة ثانية",
                "stage3": "مرحلة ثالثة",
                "stage4": "مرحلة رابعة",
            }
            await ChangeStage.stage.set()
            stages = ["مرحلة اولى","مرحلة ثانية","مرحلة ثالثة","مرحلة رابعة","الغاء التغيير"]
            stages.remove(stage_translate_revers[get_admin_stage(message.from_user.id)])
            await message.answer("أختر المرحلة التي تريد التحويل اليها", reply_markup=custom_markup(stages))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "change_stage", e)


async def change_stage_command(message, state):
    try:
        if message.text not in ["مرحلة اولى","مرحلة ثانية","مرحلة ثالثة","مرحلة رابعة","الغاء التغيير"]:
            await message.answer("أختر المرحلة من القائمة")
        else:
            stage_translate = {
                "مرحلة اولى": "stage1",
                "مرحلة ثانية": "stage2",
                "مرحلة ثالثة": "stage3",
                "مرحلة رابعة": "stage4"
            }
            stage_translate_revers = {
                "stage1": "مرحلة اولى",
                "stage2": "مرحلة ثانية",
                "stage3": "مرحلة ثالثة",
                "stage4": "مرحلة رابعة",
            }
            async with state.proxy() as data:
                data["old_stage"] = get_admin_stage(message.from_user.id)
                change_admin_stage(message.from_user.id, stage_translate[message.text])
                await message.answer("تم تغيير المرحلة بنجاح", reply_markup=admin_markup())
                await send_log(message, bot, "تغيير مرحلة", f"قام @{get_user_username(message.from_user.id)} بتغيير مرحلته من {stage_translate_revers[data['old_stage']]} الى {stage_translate_revers[get_admin_stage(message.from_user.id)]}")
            await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "change_stage_command", e)


def reg(dp):
    dp.register_message_handler(View_all_users, text="عرض جميع المستخدمين 📋")
    dp.register_message_handler(Send_anno_4all, text='أرسال اعلان للجميع 📢')
    dp.register_message_handler(Get_anno_msg_and_send, state=AnnoAll.m)
    dp.register_message_handler(Delete_manager, text ="حذف مشرف 💂")
    dp.register_message_handler(Delete_manager_get_stage, state=DelManager.stage)
    dp.register_message_handler(Delete_manager_get_uid_and_del, state=DelManager.uid)
    dp.register_message_handler(Add_manager, text="اضافة مشرف 💂")
    dp.register_message_handler(Add_manager_get_stage, state=AddManager.stage)
    dp.register_message_handler(Add_manager_get_uid_and_add, state=AddManager.uid)
    dp.register_message_handler(change_stage_canceler, text="الغاء التغيير", state=ChangeStage)
    dp.register_message_handler(change_stage, text="تغيير المرحلة 🔄")
    dp.register_message_handler(change_stage_command, state=ChangeStage.stage)



