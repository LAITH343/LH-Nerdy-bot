from aiogram.types import ContentTypes
from cmds.logger import send_log
from cmds.user_manager import get_manager_stage, check_user_stage, get_user_id, get_users_uid_by_stage, add_user, del_user, \
    check_user_exist
from cmds.markup_manager import get_user_markup, custom_markup, del_books_markup, del_extra_file_markup, manage_users_markup, manager_hwandfiles_markup, manager_markup
from cmds.classes import DelHW, AddHW, Anno, Del_File, AddNewFile, AddNewExtraFile, Del_Extra_File, AddNewUser, DelUser, UserInfo
from cmds.hw_manager import add_hw
from cmds.books_manager import add_file, del_file, get_files_list, del_extra_file, add_extra_file, get_extra_files_list
from cmds import error_reporter, user_manager
from config import bot, bot_owner

day_translate = {
            "الاحد": "sunday",
            "الاثنين": "monday",
            "الثلاثاء": "tuesday",
            "الاربعاء": "wednesday",
            "الخميس": "thursday"}


async def Manager_del_hw(message):
    try:
        if not get_manager_stage(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await DelHW.day.set()
            await message.reply("اختر اليوم", reply_markup=custom_markup(["الاحد","الاثنين","الثلاثاء","الاربعاء","الخميس","الغاء الادخال"]))# hw_day_input_markup
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Manager_del_hw", e)


async def Manager_del_hw_command(message, state):
    try:
        async with state.proxy() as data:
            data['day'] = message.text
            stage = get_manager_stage(message.from_user.id)
            add_hw(stage, day_translate[data['day']], "لا شيء")
            await message.reply("تم حذف الواجب", reply_markup=manager_markup())
            await send_log(message, bot, "حذف واجب", f"تم حذف واجب يوم {data['day']} ")
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("فشل حذف الواجب", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Manager_del_hw_command", e)


async def Manager_add_hw(message):
    try:
        if not get_manager_stage(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await AddHW.day.set()
            await message.reply("اختر اليوم", reply_markup=custom_markup(["الاحد","الاثنين","الثلاثاء","الاربعاء","الخميس","الغاء الادخال"]))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Manager_add_hw", e)


async def Manager_get_day(message, state):
    try:
        async with state.proxy() as data:
            data['day'] = message.text
    
        await AddHW.next()
        await message.reply("ارسل الواجب", reply_markup=custom_markup(["الغاء الادخال"]))# cancel_input_markup
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Manager_get_day", e)


async def Manager_add_hw_command(message, state):
    try:
        async with state.proxy() as data:
            data['hw'] = message.text
            add_hw(get_manager_stage(message.from_user.id), day_translate[data['day']], data['hw'])
            await message.reply("تم الاضافة بنجاح", reply_markup=manager_markup())
            await send_log(message, bot, "أضافة واجب", f"تم أضافة واجب يوم {data['day']} الواجب هوة {data['hw']}")
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ ما\nيرجى التحقق من المدخلات أو اذا كان لديك الصلاحيات لتنفيذ الاجراء", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Manager_add_hw_command", e)


async def Manager_send_anno(message):
    try:
        if not get_manager_stage(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await Anno.m.set()
            await message.reply("ارسل الرسالة التي تريد اعلانها", reply_markup=custom_markup(["الغاء الادخال"]))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Manager_send_anno", e)


async def Manager_send_anno_command(message, state):
    try:
        async with state.proxy() as data:
            data['m'] = f"أعلان  📢 بواسطة: @{message.from_user.username}\n\n"
            data['m'] += message.text
            for user in get_users_uid_by_stage(get_manager_stage(message.from_user.id)):
                await bot.send_message(user, data['m'])
            await message.reply("تم ارسال الاعلان بنجاح", reply_markup=manager_markup())
            await send_log(message, bot, "ارسال اعلان للمرحلة", f"الأعلان الذي تم ارساله \n{data['m']}")
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("فشل ارسال الاعلان", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Manager_send_anno_command", e)


async def Add_book(message):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await AddNewFile.file_name.set()
            await bot.send_message(message.chat.id, "ارسل اسم الملف الذي يظهر للاخرين", reply_markup=custom_markup(["الغاء الاضافة"]))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_book", e)


async def Add_book_get_file_name(message, state):
    try:
        if not message.text:
            await message.answer("ارسل اسم الملف اولا")
        elif len(message.text) > 20:
            await message.answer("الاسم لا يمكن أن يكون أكثر من 20 حرف!")
        else:
            async with state.proxy() as data:
                data["file_name"] = message.text

            await AddNewFile.next()
            await bot.send_message(message.chat.id, "ارسل الملف", reply_markup=custom_markup(["الغاء الاضافة"]))
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_book_get_file_name", e)


async def Add_book_command(message, state):
    try:
        if document := message.document:
            await message.answer("جاري تنزيل الملف")
            await document.download(
                destination_file=f"storage/books/{get_manager_stage(message.from_user.id)}/{document.file_name}",)

        async with state.proxy() as data:
            data["file_path"] = f"storage/books/{get_manager_stage(message.from_user.id)}/{document.file_name}"

            await add_file(get_manager_stage(message.from_user.id), data["file_name"], data["file_path"])
            await state.finish()
            await bot.send_message(message.chat.id, "تم اضافة الملف بنجاح", reply_markup=manager_markup())
            await send_log(message, bot, "أضافة كتاب", f"تم أضافة كتاب {data['file_name']}")
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_book_command", e)


async def del_book(message):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("عذرا ليس لديك الصلاحيات لأجراء هذا الامر", reply_markup=get_user_markup(message.from_user.id))
        else:
            await Del_File.temp.set()
            await message.answer("اختر الملف الذي تريد حذفه من القائمة", reply_markup=del_books_markup(get_files_list(check_user_stage(message.from_user.id))))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "del_book", e)


async def del_book_command(message, state):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("عذرا ليس لديك الصلاحيات لأجراء هذا الامر", reply_markup=get_user_markup(message.from_user.id))
        else:
            if message.text == "الرجوع للقائمة الرئيسية 🏠":
                await message.answer("تم الرجوع الى القائمة الرئيسية", reply_markup=get_user_markup(message.from_user.id))
            else:
                await del_file(get_manager_stage(message.from_user.id),message.text)
                await message.answer("تم حذف الكتاب", reply_markup=manager_markup())
                await send_log(message, bot, "حذف كتاب", f"تم حذف كتاب {message.text}")
            await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("فشل حذف الملف", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "del_book_command", e)


async def Add_extra_file(message):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await AddNewExtraFile.file_name.set()
            await bot.send_message(message.chat.id, "ارسل اسم الملف الذي يظهر للاخرين", reply_markup=custom_markup(["الغاء الاضافة"]))
    except Exception as e:
        await message.answer("فشل حذف الملف", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_extra_file", e)


async def Add_extra_file_get_file_name(message, state):
    try:
        if not message.text:
            await message.answer("ارسل اسم الملف اولا")
        elif len(message.text) > 20:
            await message.answer("الاسم لا يمكن أن يكون أكثر من 20 حرف!")
        else:
            async with state.proxy() as data:
                data["file_name"] = message.text

            await AddNewExtraFile.next()
            await bot.send_message(message.chat.id, "ارسل الملف", reply_markup=custom_markup(["الغاء الاضافة"]))
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_extra_file_get_file_name", e)


async def Add_extra_file_command(message, state):
    try:
        if document := message.document:
            await message.answer("جاري تنزيل الملف")
            await document.download(
                destination_file=f"storage/extra/{get_manager_stage(message.from_user.id)}/{document.file_name}",)

        async with state.proxy() as data:
            data["file_path"] = f"storage/extra/{get_manager_stage(message.from_user.id)}/{document.file_name}"

            await add_extra_file(get_manager_stage(message.from_user.id), data["file_name"], data["file_path"])
            await state.finish()
            await bot.send_message(message.chat.id, "تم اضافة الملف بنجاح", reply_markup=manager_markup())
            await send_log(message, bot, "أضافة ملف", f"تم أضافة ملف {data['file_name']}")
    except Exception as e:
        await state.finish()
        await message.answer("فشل اضافة الملف", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_extra_file_command", e)


async def Del_extra_file(message):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("عذرا ليس لديك الصلاحيات لأجراء هذا الامر", reply_markup=get_user_markup(message.from_user.id))
        else:
            await Del_Extra_File.temp.set()
            await message.answer("اختر الملف الذي تريد حذفه من القائمة", reply_markup=del_extra_file_markup(get_extra_files_list(check_user_stage(message.from_user.id))))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Del_extra_file", e)


async def del_extra_file_command(message, state):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("عذرا ليس لديك الصلاحيات لأجراء هذا الامر", reply_markup=get_user_markup(message.from_user.id))
        else:
            if message.text == "الرجوع للقائمة الرئيسية 🏠":
                await message.answer("تم الرجوع الى القائمة الرئيسية", reply_markup=get_user_markup(message.from_user.id))
            else:
                await del_extra_file(get_manager_stage(message.from_user.id),message.text)
                await message.answer("تم حذف الملف", reply_markup=get_user_markup(message.from_user.id))
                await send_log(message, bot, "حذف ملف", f"تم حذف الملف {message.text}")
            await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "del_extra_file_command", e)


async def Add_New_user(message):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await AddNewUser.uid.set()
            await message.answer("ارسل ID الطالب", reply_markup=custom_markup(["الغاء أضافة الطالب"]))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_New_user", e)


async def Add_New_user_command(message, state):
    try:
        if not message.text.isdigit():
            await message.answer("يرجى ارسال ارقام فقط")
        elif check_user_exist(message.text):
            await message.answer("المستخدم موجود بالفعل")
        else:
            translate = {
                "stage1": "اولى",
                "stage2": "ثانية",
                "stage3": "ثالثة",
                "stage4": "رابعة",
            }
            async with state.proxy() as data:
                data["uid"] = message.text
                add_user(get_manager_stage(message.from_user.id), data["uid"], "notset", "notset")
            await state.finish()
            await message.answer("تم أضافة الطالب", reply_markup=manager_markup())
            await send_log(message, bot, "أضافة طالب", f"تم أضافة {data['uid']} للمرحلة {translate[get_manager_stage(message.from_user.id)]}")
            await bot.send_message(int(message.text), "مرحبا\nتم أضافتك, لبدء الاستخدام أرسل 'بدء' أو اضغط على /start")
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_New_user_command", e)


async def Del_user(message):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await DelUser.uid.set()
            await message.answer("ارسل ID الطالب", reply_markup=custom_markup(["الغاء حذف الطالب"]))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Del_user", e)


async def Del_user_command(message, state):
    try:
        if not message.text.isdigit():
            await message.answer("يرجى ارسال ارقام فقط")
        elif not check_user_exist(message.text):
            await message.answer("المستخدم غير موجود")
        elif check_user_stage(message.text) != get_manager_stage(message.from_user.id):
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
                data["uid"] = message.text
                del_user(data["uid"], get_manager_stage(message.from_user.id))
            await state.finish()
            await message.answer("تم حذف الطالب", reply_markup=manager_markup())
            await send_log(message, bot, "حذف طالب",f"تم حذف {data['uid']} من المرحلة  {translate[get_manager_stage(message.from_user.id)]}")
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Del_user_command", e)


async def cancel_del_user(message, state):
    await state.finish()
    await message.answer("تم الغاء الحذف", reply_markup=manager_markup())


async def cancel_add_user(message, state):
    await state.finish()
    await message.answer("تم الغاء الادخال", reply_markup=manager_markup())


async def cancel_del_file(message, state):
    if not user_manager.get_manager_stage(message.from_user.id):
        await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
    else:
        await state.finish()
        await message.answer("تم الالغاء بنجاح", reply_markup=manager_markup())


async def cancel_del_book(message, state):
    try:
        if not user_manager.get_manager_stage(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء",
                                 reply_markup=get_user_markup(message.from_user.id))
        else:
            await state.finish()
            await message.answer("تم الالغاء بنجاح", reply_markup=manager_markup())
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "main - delete book canceler", e)


async def cancel_handler(message, state):
    try:
        # Cancel state
        await state.finish()
        await message.reply('تم الغاء الاضافة', reply_markup=manager_markup())
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "main - add book cancler ", e)


async def cancel_Book_handler(message, state):
    try:
        # Cancel state
        await state.finish()
        await message.reply('تم الغاء الاضافة', reply_markup=manager_markup())
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "add book cancler ", e)


async def files_and_hw_markup(message):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء")
        else:
            await message.answer("تم عرض القائمة", reply_markup=manager_hwandfiles_markup())
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "files_and_hw_markup ", e)


async def manage_user_markup(message):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء")
        else:
            await message.answer("تم عرض القائمة", reply_markup=manage_users_markup())
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "files_and_hw_markup ", e)


async def back_to_manager_markup(message):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء")
        else:
            await message.answer("تم عرض صلاحيات المشرف", reply_markup=manager_markup())
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "back_to_manager_markup ", e)


async def get_user_info(message):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء")
        else:
            await UserInfo.id.set()
            await message.answer("أرسل معرف الطالب (بدون ال@) أو الID", reply_markup=custom_markup(["الغاء البحث"]))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "get_user_info ", e)


async def get_user_info_id(message, state):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء")
        elif not message.text.isdigit():
            uid = get_user_id(message.text)
            if get_manager_stage(message.from_user.id) != check_user_stage(uid):
                await message.answer("لم يتم العثور على الطالب")
            else:
                uinfo = await bot.get_chat(uid)
                await message.answer(f"name: {uinfo.full_name}\nid: {uinfo.id}", reply_markup=manager_markup())
                await state.finish()
        elif get_manager_stage(message.from_user.id) != check_user_stage(message.text):
            await message.answer("لم يتم العثور على الطالب")
        else:
            uinfo = await bot.get_chat(message.text)
            await message.answer(f"name: {uinfo.full_name}\nusername: @{uinfo.username}", reply_markup=manager_markup())
            await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "get_user_info_id ", e)


async def user_info_cancel(message, state):
    await state.finish()
    await message.answer("تم الغاء البحث", reply_markup=manager_markup())



def reg(dp):
    dp.register_message_handler(cancel_Book_handler, text='الغاء الاضافة', state=AddNewFile)
    dp.register_message_handler(cancel_handler, text='الغاء الاضافة', state=AddNewExtraFile)
    dp.register_message_handler(Manager_del_hw, text="حذف واجب 📝")
    dp.register_message_handler(Manager_del_hw_command, state=DelHW.day)
    dp.register_message_handler(Manager_add_hw, text = "اضافة واجب 📝")
    dp.register_message_handler(Manager_get_day, state=AddHW.day)
    dp.register_message_handler(Manager_add_hw_command, state=AddHW.hw)
    dp.register_message_handler(Manager_send_anno, text="أرسال اعلان 📢")
    dp.register_message_handler(Manager_send_anno_command, state=Anno.m)
    dp.register_message_handler(cancel_del_book, text="الغاء الحذف", state=Del_File)
    dp.register_message_handler(Add_book, text="اضافة كتاب 📕")
    dp.register_message_handler(Add_book_get_file_name, state=AddNewFile.file_name, content_types=ContentTypes.ANY)
    dp.register_message_handler(Add_book_command, state=AddNewFile.file_path, content_types=ContentTypes.DOCUMENT)
    dp.register_message_handler(cancel_del_file, text="الغاء حذف الملف", state=Del_Extra_File)
    dp.register_message_handler(del_book, text = "حذف كتاب ❌")
    dp.register_message_handler(del_book_command, state=Del_File.temp)
    dp.register_message_handler(Add_extra_file, text = "اضافة ملف 📎")
    dp.register_message_handler(Add_extra_file_get_file_name, state=AddNewExtraFile.file_name, content_types=ContentTypes.ANY)
    dp.register_message_handler(Add_extra_file_command, state=AddNewExtraFile.file_path, content_types=ContentTypes.DOCUMENT)
    dp.register_message_handler(Del_extra_file, text = "حذف ملف ❌")
    dp.register_message_handler(del_extra_file_command, state=Del_Extra_File.temp)
    dp.register_message_handler(cancel_add_user, text="الغاء أضافة الطالب", state=AddNewUser)
    dp.register_message_handler(Add_New_user, text = "أضافة طالب")
    dp.register_message_handler(Add_New_user_command, state=AddNewUser.uid)
    dp.register_message_handler(cancel_del_user, text="الغاء حذف الطالب", state=DelUser)
    dp.register_message_handler(Del_user, text="حذف طالب")
    dp.register_message_handler(Del_user_command, state=DelUser.uid)
    dp.register_message_handler(files_and_hw_markup, text="الواجبات و الملفات")
    dp.register_message_handler(manage_user_markup, text="أدارة الطلاب")
    dp.register_message_handler(back_to_manager_markup, text="الرجوع الى صلاحيات المشرف")
    dp.register_message_handler(user_info_cancel, text="الغاء البحث", state=UserInfo)
    dp.register_message_handler(get_user_info, text="عرض معلومات طالب")
    dp.register_message_handler(get_user_info_id, state=UserInfo.id)
