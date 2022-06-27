from cmds.user_manager import get_manager_stage, check_user_stage, get_users_uid_by_stage
from cmds.markup_manager import get_user_markup, custom_markup, del_books_markup, del_extra_file_markup
from cmds.classes import DelHW, AddHW, Anno, Del_File, AddNewFile, AddNewExtraFile, Del_Extra_File
from cmds.hw_adder import add_hw
from cmds.books_manager import add_file, del_file, get_files_list, del_extra_file, add_extra_file, get_extra_files_list
from cmds import error_reporter


async def Manager_del_hw(message, bot):
    try:
        if not get_manager_stage(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await DelHW.day.set()
            await message.reply("اختر اليوم", reply_markup=custom_markup(["الاحد","الاثنين","الثلاثاء","الاربعاء","الخميس","الغاء الادخال"]))# hw_day_input_markup
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Manager_del_hw", e)


async def Manager_del_hw_command(message, state, bot):
    try:
        async with state.proxy() as data:
            data['day'] = message.text
            stage = get_manager_stage(message.from_user.id)
            add_hw(stage, data['day'], "لا شيء")
            await message.reply("تم حذف الواجب", reply_markup=get_user_markup(message.from_user.id))
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("فشل حذف الواجب", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Manager_del_hw_command", e)


async def Manager_add_hw(message, bot):
    try:
        if not get_manager_stage(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await AddHW.day.set()
            await message.reply("اختر اليوم", reply_markup=custom_markup(["الاحد","الاثنين","الثلاثاء","الاربعاء","الخميس","الغاء الادخال"]))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Manager_add_hw", e)


async def Manager_get_day(message, state, bot):
    try:
        async with state.proxy() as data:
            data['day'] = message.text
    
        await AddHW.next()
        await message.reply("ارسل الواجب", reply_markup=custom_markup(["الغاء الادخال"]))# cancel_input_markup
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Manager_get_day", e)


async def Manager_add_hw_command(message, state, bot):
    try:
        async with state.proxy() as data:
            data['hw'] = message.text
            add_hw(get_manager_stage(message.from_user.id), data['day'], data['hw'])
            await message.reply("تم الاضافة بنجاح", reply_markup=get_user_markup(message.from_user.id))
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ ما\nيرجى التحقق من المدخلات أو اذا كان لديك الصلاحيات لتنفيذ الاجراء", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Manager_add_hw_command", e)


async def Manager_send_anno(message, bot):
    try:
        if not get_manager_stage(message.from_user.id):
            await bot.send_message(message.chat.id, "عذرا ليس لديك صلاحية ﻷتمام هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await Anno.m.set()
            await message.reply("ارسل الرسالة التي تريد اعلانها", reply_markup=custom_markup(["الغاء الادخال"]))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Manager_send_anno", e)


async def Manager_send_anno_command(message, state, bot):
    try:
        async with state.proxy() as data:
            data['m'] = f"أعلان  📢 بواسطة: @{message.from_user.username}\n\n"
            data['m'] += message.text
            for user in get_users_uid_by_stage(get_manager_stage(message.from_user.id)):
                await bot.send_message(user, data['m'])
            await message.reply("تم ارسال الاعلان بنجاح", reply_markup=get_user_markup(message.from_user.id))
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("فشل ارسال الاعلان", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Manager_send_anno_command", e)


async def Add_book(message, bot):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await AddNewFile.file_name.set()
            await bot.send_message(message.chat.id, "ارسل اسم الملف الذي يظهر للاخرين", reply_markup=custom_markup(["الغاء الاضافة"]))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_book", e)


async def Add_book_get_file_name(message, state, bot):
    try:
        async with state.proxy() as data:
            data["file_name"] = message.text

        await AddNewFile.next()
        await bot.send_message(message.chat.id, "ارسل الملف", reply_markup=custom_markup(["الغاء الاضافة"]))
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_book_get_file_name", e)


async def Add_book_command(message, state, bot):
    try:
        if document := message.document:
            await message.answer("جاري تنزيل الملف")
            await document.download(
                destination_file=f"storage/books/{get_manager_stage(message.from_user.id)}/{document.file_name}",)

        async with state.proxy() as data:
            data["file_path"] = f"storage/books/{get_manager_stage(message.from_user.id)}/{document.file_name}"

            await add_file(get_manager_stage(message.from_user.id), data["file_name"], data["file_path"])
            await state.finish()
            await bot.send_message(message.chat.id, "تم اضافة الملف بنجاح", reply_markup=get_user_markup(message.from_user.id))
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_book_command", e)


async def del_book(message, bot):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("عذرا ليس لديك الصلاحيات لأجراء هذا الامر", reply_markup=get_user_markup(message.from_user.id))
        else:
            await Del_File.temp.set()
            await message.answer("اختر الملف الذي تريد حذفه من القائمة", reply_markup=del_books_markup(get_files_list(check_user_stage(message.from_user.id))))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "del_book", e)


async def del_book_command(message, state, bot):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("عذرا ليس لديك الصلاحيات لأجراء هذا الامر", reply_markup=get_user_markup(message.from_user.id))
        else:
            if message.text == "الرجوع للقائمة الرئيسية 🏠":
                await message.answer("تم الرجوع الى القائمة الرئيسية", reply_markup=get_user_markup(message.from_user.id))
            else:
                await del_file(get_manager_stage(message.from_user.id),message.text)
                await message.answer("تم حذف الكتاب", reply_markup=get_user_markup(message.from_user.id))
            await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("فشل حذف الملف", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "del_book_command", e)



async def Add_extra_file(message, bot):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء", reply_markup=get_user_markup(message.from_user.id))
        else:
            await AddNewExtraFile.file_name.set()
            await bot.send_message(message.chat.id, "ارسل اسم الملف الذي يظهر للاخرين", reply_markup=custom_markup(["الغاء الاضافة"]))
    except Exception as e:
        await message.answer("فشل حذف الملف", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_extra_file", e)


async def Add_extra_file_get_file_name(message, state, bot):
    try:
        async with state.proxy() as data:
            data["file_name"] = message.text

        await AddNewExtraFile.next()
        await bot.send_message(message.chat.id, "ارسل الملف", reply_markup=custom_markup(["الغاء الاضافة"]))
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_extra_file_get_file_name", e)


async def Add_extra_file_command(message, state, bot):
    try:
        if document := message.document:
            await message.answer("جاري تنزيل الملف")
            await document.download(
                destination_file=f"storage/extra/{get_manager_stage(message.from_user.id)}/{document.file_name}",)

        async with state.proxy() as data:
            data["file_path"] = f"storage/extra/{get_manager_stage(message.from_user.id)}/{document.file_name}"

            await add_extra_file(get_manager_stage(message.from_user.id), data["file_name"], data["file_path"])
            await state.finish()
            await bot.send_message(message.chat.id, "تم اضافة الملف بنجاح", reply_markup=get_user_markup(message.from_user.id))
    except Exception as e:
        await state.finish()
        await message.answer("فشل اضافة الملف", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Add_extra_file_command", e)


async def Del_extra_file(message, bot):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("عذرا ليس لديك الصلاحيات لأجراء هذا الامر", reply_markup=get_user_markup(message.from_user.id))
        else:
            await Del_Extra_File.temp.set()
            await message.answer("اختر الملف الذي تريد حذفه من القائمة", reply_markup=del_extra_file_markup(get_extra_files_list(check_user_stage(message.from_user.id))))
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Del_extra_file", e)


async def del_extra_file_command(message, state, bot):
    try:
        if not get_manager_stage(message.from_user.id):
            await message.answer("عذرا ليس لديك الصلاحيات لأجراء هذا الامر", reply_markup=get_user_markup(message.from_user.id))
        else:
            if message.text == "الرجوع للقائمة الرئيسية 🏠":
                await message.answer("تم الرجوع الى القائمة الرئيسية", reply_markup=get_user_markup(message.from_user.id))
            else:
                await del_extra_file(get_manager_stage(message.from_user.id),message.text)
                await message.answer("تم حذف الملف", reply_markup=get_user_markup(message.from_user.id))
            await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "del_extra_file_command", e)
