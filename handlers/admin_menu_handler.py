import os
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Utility.logger import send_log
from Utility.statistics import get_bot_users
from Utility.user_manager import get_all_usernames, check_admin, del_manager, add_manager, get_user_full_info, get_user_id, get_users_uid, \
    get_user_username, change_admin_stage, get_admin_stage, add_user, check_user_exist, check_user_stage, del_user
from Utility.markup_manager import admin_user_mangment, get_user_markup, custom_markup, admin_markup
from Utility import error_reporter
from config import bot, bot_owner

class AddManager(StatesGroup):
	stage = State()
	uid = State()

class AdminUserInfo(StatesGroup):
	id = State()

class AnnoAll(StatesGroup):
	m = State()

class DelManager(StatesGroup):
	stage = State()
	uid = State()

class ChangeStage(StatesGroup):
	stage = State()
	old_stage = State()

class DelUserByAdmin(StatesGroup):
	stage = State()
	uid = State()

class AddNewUserByAdmin(StatesGroup):
	stage = State()
	uid = State()


async def View_all_users(message):
    try:
        if not check_admin(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            file = await get_bot_users()
            await bot.send_document(message.from_user.id, document=open(file, 'rb'))
            os.remove(file)
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
            await message.reply("اختر المرحلة", reply_markup=custom_markup(["مرحلة اولى","مرحلة ثانية","مرحلة ثالثة","مرحلة رابعة","الغاء الحذف"]))
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
                await message.reply("تم الحذف بنجاح", reply_markup=admin_user_mangment())
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
            await message.reply("اختر المرحلة", reply_markup=custom_markup(["مرحلة اولى","مرحلة ثانية","مرحلة ثالثة","مرحلة رابعة","الغاء اضافة مشرف"])) # add_del_man_stage_input_markup
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
                await message.reply("تم الاضافة بنجاح", reply_markup=admin_user_mangment())
                await send_log(message, bot, "أضافة مشرف", f"تم أضافة @{get_user_username(data['uid'])} مشرف للمرحلة {translate[data['stage']]}")
            await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("فشل اضافة المشرف", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_manager_get_uid_and_add", e)


async def change_stage_canceler(message, state):
    try:
        await state.finish()
        await message.answer("تم الغاء التغيير", reply_markup=admin_user_mangment())
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
                await message.answer("تم تغيير المرحلة بنجاح", reply_markup=admin_user_mangment())
                await send_log(message, bot, "تغيير مرحلة", f"قام @{get_user_username(message.from_user.id)} بتغيير مرحلته من {stage_translate_revers[data['old_stage']]} الى {stage_translate_revers[get_admin_stage(message.from_user.id)]}")
            await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "change_stage_command", e)


async def add_user_by_admin(message):
    try:
        if not check_admin(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء")
        else:
            await AddNewUserByAdmin.stage.set()
            await message.answer("أختر المرحلة", reply_markup=custom_markup(["مرحلة اولى","مرحلة ثانية","مرحلة ثالثة","مرحلة رابعة","الغاء أضافة الطالب"]))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "add_user_by_admin", e)


async def add_user_by_admin_stage(message, state):
    try:
        if message.text not in ["مرحلة اولى","مرحلة ثانية","مرحلة ثالثة","مرحلة رابعة","الغاء أضافة الطالب"]:
            await message.answer("أختر من القائمة")
        else:
            stage_translate = {
                "مرحلة اولى": "stage1",
                "مرحلة ثانية": "stage2",
                "مرحلة ثالثة": "stage3",
                "مرحلة رابعة": "stage4"
            }
            async with state.proxy() as data:
                data['stage'] = stage_translate[message.text]
            await AddNewUserByAdmin.next()
            await message.answer("أرسل ID المستخدم", reply_markup=custom_markup(["الغاء أضافة الطالب"]))
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "add_user_by_admin_stage", e)


async def add_user_by_admin_command(message, state):
    try:
        if not message.text.isdigit():
            await message.answer("أرسل أرقام فقط!")
        elif check_user_exist(message.text):
            await message.answer("المستخدم موجود بالفعل!")
        else:
            stage_translate_revers = {
                "stage1": "مرحلة اولى",
                "stage2": "مرحلة ثانية",
                "stage3": "مرحلة ثالثة",
                "stage4": "مرحلة رابعة",
            }
            async with state.proxy() as data:
                add_user(data['stage'], message.text, "notset", "notset")
                await message.answer("تم أضافة المستخدم بنجاح", reply_markup=admin_user_mangment())
                await bot.send_message(int(message.text), "مرحبا\nتم أضافتك, لبدء الاستخدام أرسل 'بدء' أو اضغط على /start")
                await send_log(message, bot, "أضافة مستخدم", f"تم أضافة {message.text} الى  {stage_translate_revers[data['stage']]}")
            await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "add_user_by_admin_command", e)


async def add_user_by_admin_canceler(message, state):
    await state.finish()
    await message.answer("تم الالغاء", reply_markup=admin_user_mangment())


async def Del_user_by_admin(message):
    try:
        if not check_admin(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await DelUserByAdmin.stage.set()
            await message.answer("أختر المرحلة", reply_markup=custom_markup(["مرحلة اولى","مرحلة ثانية","مرحلة ثالثة","مرحلة رابعة","الغاء حّذف الطالب"]))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Del_user_by_admin", e)


async def Del_user_by_admin_stage(message, state):
    try:
        if message.text not in ["مرحلة اولى","مرحلة ثانية","مرحلة ثالثة","مرحلة رابعة","الغاء حّذف الطالب"]:
            await message.answer("أختر من القائمة")
        else:
            stage_translate = {
                "مرحلة اولى": "stage1",
                "مرحلة ثانية": "stage2",
                "مرحلة ثالثة": "stage3",
                "مرحلة رابعة": "stage4"
            }
            async with state.proxy() as data:
                data['stage'] = stage_translate[message.text]
            await DelUserByAdmin.next()
            await message.answer("أرسل ID الطالب")
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Del_user_by_admin_stage", e)


async def Del_user_by_admin_command(message, state):
    try:
        if not message.text.isdigit():
            await message.answer("يرجى ارسال ارقام فقط")
        elif not check_user_exist(message.text):
            await message.answer("المستخدم غير موجود")
        elif int(message.text) == int(bot_owner):
            await message.answer("لا يمكنك حذف مالك البوت")
        else:
            translate = {
                "stage1": "اولى",
                "stage2": "ثانية",
                "stage3": "ثالثة",
                "stage4": "رابعة",
            }
            async with state.proxy() as data:
                del_user(message.text, data['stage'])
                await message.answer("تم حذف الطالب", reply_markup=admin_user_mangment())
                await send_log(message, bot, "حذف طالب",f"تم حذف {message.text} من المرحلة  {translate[data['stage']]}")
            await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Del_user_by_admin_command", e)


async def del_user_by_admin_canceler(message, state):
    await state.finish()
    await message.answer("تم الالغاء", reply_markup=admin_user_mangment())


async def admin_get_user_info(message):
    try:
        if not check_admin(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء")
        else:
            await AdminUserInfo.id.set()
            await message.answer("أرسل معرف الطالب (بدون ال@) أو الID", reply_markup=custom_markup(["الغاء البحث"]))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "admin_get_user_info ", e)


async def admin_get_user_info_id(message, state):
    try:
        if not check_admin(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء")
        elif not message.text.isdigit():
            uid = get_user_id(message.text)
            if not check_user_exist(uid):
                await message.answer("لم يتم العثور على الطالب")
            else:
                Stagetranslate = {
                    "stage1": "اولى",
                    "stage2": "ثانية",
                    "stage3": "ثالثة",
                    "stage4": "رابعة",
                    "False": "لا",
                    "True": "نعم"
                }
                tfTran = {
                    "True": "نعم",
                    "False": "لا"
                }
                uinfo = await bot.get_chat(uid)
                full_info = get_user_full_info(uid)
                await message.answer(f"الاسم: {uinfo.full_name}\nالأي دي: {uinfo.id}\nالمرحلة: {Stagetranslate[full_info[3]]}\nمشرف؟: {tfTran[full_info[4]]}\nأدمن؟: {tfTran[full_info[5]]}", reply_markup=admin_user_mangment())
                await state.finish()
        elif not check_user_exist(message.text):
            await message.answer("لم يتم العثور على الطالب")
        else:
            Stagetranslate = {
                "stage1": "اولى",
                "stage2": "ثانية",
                "stage3": "ثالثة",
                "stage4": "رابعة",
                "False": "لا",
                "True": "نعم"
            }
            tfTran = {
                "True": "نعم",
                "False": "لا"
            }
            uinfo = await bot.get_chat(message.text)
            full_info = get_user_full_info(message.text)
            await message.answer(f"الاسم: {uinfo.full_name}\nالمرحلة: {Stagetranslate[full_info[3]]}\nالمعرف(اليوزر): @{uinfo.username}\nمشرف؟: {tfTran[full_info[4]]}\nأدمن؟: {tfTran[full_info[5]]}", reply_markup=admin_user_mangment())
            await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "admin_get_user_info_id ", e)


async def user_info_cancel(message, state):
    await state.finish()
    await message.answer("تم الغاء البحث", reply_markup=admin_user_mangment())


async def show_users_markup(message):
    if not check_admin(message.from_user.id):
        await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء")
    else:
        await message.answer("تم عرض القائمة", reply_markup=admin_user_mangment())


async def back_to_admin_markup(message):
    if not check_admin(message.from_user.id):
        await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء")
    else:
        await message.answer("تم عرض صلاحيات الادمن", reply_markup=admin_markup())


async def cancel_add_manager(message, state):
    if not check_admin(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
    else:
        await state.finish()
        await message.answer("تم الغاء الاضافة", reply_markup=admin_user_mangment())


async def cancel_del_manager(message, state):
    if not check_admin(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
    else:
        await state.finish()
        await message.answer("تم الغاء الحذف", reply_markup=admin_user_mangment())


def reg(dp):
    dp.register_message_handler(View_all_users, text="عرض جميع المستخدمين 📋")
    dp.register_message_handler(Send_anno_4all, text='أرسال اعلان للجميع 📢')
    dp.register_message_handler(Get_anno_msg_and_send, state=AnnoAll.m)
    dp.register_message_handler(cancel_del_manager, state=DelManager, text="الغاء الحذف")
    dp.register_message_handler(Delete_manager, text ="حذف مشرف 💂")
    dp.register_message_handler(Delete_manager_get_stage, state=DelManager.stage)
    dp.register_message_handler(Delete_manager_get_uid_and_del, state=DelManager.uid)
    dp.register_message_handler(cancel_add_manager, state=AddManager, text="الغاء اضافة مشرف")
    dp.register_message_handler(Add_manager, text="اضافة مشرف 💂")
    dp.register_message_handler(Add_manager_get_stage, state=AddManager.stage)
    dp.register_message_handler(Add_manager_get_uid_and_add, state=AddManager.uid)
    dp.register_message_handler(change_stage_canceler, text="الغاء التغيير", state=ChangeStage)
    dp.register_message_handler(change_stage, text="تغيير المرحلة 🔄")
    dp.register_message_handler(change_stage_command, state=ChangeStage.stage)
    dp.register_message_handler(add_user_by_admin_canceler, text="الغاء أضافة الطالب", state=AddNewUserByAdmin)
    dp.register_message_handler(add_user_by_admin, text="أضافة طالب جديد")
    dp.register_message_handler(add_user_by_admin_stage, state=AddNewUserByAdmin.stage)
    dp.register_message_handler(add_user_by_admin_command, state=AddNewUserByAdmin.uid)
    dp.register_message_handler(del_user_by_admin_canceler,text="الغاء حّذف الطالب", state=DelUserByAdmin)
    dp.register_message_handler(Del_user_by_admin, text="حّذف طالب")
    dp.register_message_handler(Del_user_by_admin_stage, state=DelUserByAdmin.stage)
    dp.register_message_handler(Del_user_by_admin_command, state=DelUserByAdmin.uid)
    dp.register_message_handler(user_info_cancel, text="الغاء البحث", state=AdminUserInfo)
    dp.register_message_handler(show_users_markup, text="ادارة الطلاب")
    dp.register_message_handler(back_to_admin_markup, text="الرجوع الى صلاحيات الادمن")
    dp.register_message_handler(admin_get_user_info, text="عرض معلومات مفصلة عن طالب")
    dp.register_message_handler(admin_get_user_info_id, state=AdminUserInfo.id)
    






