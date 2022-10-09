import random
import shutil
import string
import os
from aiogram.types import ContentTypes
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Utility.user_manager import check_user_exist
from Utility.markup_manager import get_user_markup, custom_markup
from Utility.pdf_manager import images_to_pdf, merge_pdfs
from Utility import error_reporter
from config import bot


class MergePdf(StatesGroup):
    folder = State()
    file_name = State()
    temp = State()


class MergeImages(StatesGroup):
    folder = State()
    file_name = State()
    count = State()
    temp = State()


async def get_files_count(path: string):
    return len(os.listdir(path)) - 1


async def Imgs2Pdf_file_name(message, state):
    try:
        await MergeImages.folder.set()
        randfile = ''.join(random.choice(string.ascii_lowercase)
                           for i in range(20))
        os.mkdir(f"cache/{randfile}")
        async with state.proxy() as data:
            data['folder'] = f"cache/{randfile}"
        await MergeImages.next()
        await message.reply("ماذا تريد ان تسمي الملف؟", reply_markup=custom_markup(["الغاء الدمج"]))
    except Exception as e:
        async with state.proxy() as data:
            shutil.rmtree(data['folder'])
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Imgs2Pdf_file_name", e)


async def Imgs2Pdf_get_images(message, state):
    try:
        async with state.proxy() as data:
            if document := message.document:
                await message.answer("يرجى ارسال الاسم أولا")
                return
            elif photo := message.photo:
                await message.answer("يرجى ارسال الاسم أولا")
                return
            data['file_name'] = message.text
            open(f"{data['folder']}/files", "a+").close()
        await MergeImages.temp.set()
        await message.reply("ارسل الصور وعند الرد على جميع الصور برسالة 'تم تنزيل الملف' يمكنك ارسل أو ضعط دمج", reply_markup=custom_markup(["دمج", "الغاء الدمج"]))
    except Exception as e:
        async with state.proxy() as data:
            shutil.rmtree(data['folder'])
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Imgs2Pdf_get_images", e)


async def Imgs2Pdf_cancel_handler(message, state):
    try:
        async with state.proxy() as data:
            shutil.rmtree(data['folder'])
            await message.reply("تم الغاء الدمج وحذف الملفات", reply_markup=get_user_markup(message.from_user.id))
        await state.finish()
    except Exception as e:
        async with state.proxy() as data:
            shutil.rmtree(data['folder'])
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Imgs2Pdf_cancel_handler", e)


async def Imgs2Pdf_Imgs_downloader(message, state):
    try:
        async with state.proxy() as data:
            if document := message.document:
                await document.download(destination_file=f"{data['folder']}/{document.file_name}",)
                pic_count = await get_files_count(data['folder'])
                await message.reply(f"تم تنزيل الملف عدد الصور الكلي {pic_count}")
                with open((data['folder'] + "/files"), 'a+') as fls:
                    fls.write(f"{data['folder']}/{document.file_name};")
                    fls.close()

            elif photo := message.photo:
                rand_name = ''.join(random.choice(
                    string.ascii_lowercase) for i in range(10))
                await photo[-1].download(destination_file=f"{data['folder']}/{rand_name}",)
                pic_count = await get_files_count(data['folder'])
                await message.reply(f"تم تنزيل الملف عدد الصور الكلي {pic_count}")
                with open((data['folder'] + "/files"), 'a+') as fls:
                    fls.write(f"{data['folder']}/{rand_name};")
                    fls.close()
            else:
                await message.answer("الرجاء ارسال صورة")
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Imgs2Pdf_Imgs_downloader", e)


async def Imgs2Pdf_merge_handler(message, state):
    try:
        async with state.proxy() as data:
            pic_count = await get_files_count(data['folder'])
            if pic_count == 0:
                await message.answer("يرجى ارسال صورة واحدة كحد ادنى")
                return
            f = open((data['folder'] + "/files"), 'r')
            file = f.read()
            f.close()
            pdfs = file.split(";")
            pdfs.remove('')
            await bot.send_message(message.chat.id, "جاري دمج الصور و رفع الملف")
            await bot.send_document(message.chat.id, document=open(images_to_pdf(pdfs, data['folder'], data['file_name']), 'rb'), reply_markup=get_user_markup(message.from_user.id))
            shutil.rmtree(data['folder'])
        await state.finish()
    except Exception as e:
        async with state.proxy() as data:
            shutil.rmtree(data['folder'])
        await state.finish()
        await message.answer("فشل دمج الملفات", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Imgs2Pdf_merge_handler", e)


async def MergePdf_ask_file_name(message, state):
    try:
        if not check_user_exist(message.from_user.id):
            await message.reply("اختر المرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
        else:
            await MergePdf.folder.set()
            randfile = ''.join(random.choice(string.ascii_lowercase)
                               for i in range(20))
            os.mkdir(f"cache/{randfile}")
            async with state.proxy() as data:
                data['folder'] = f"cache/{randfile}"
            await MergePdf.next()
            await message.reply("ماذا تريد ان تسمي الملف؟", reply_markup=custom_markup(["الغاء الدمج"]))
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "MergePdf_ask_file_name", e)


async def MergePdf_get_file_name(message, state):
    try:
        async with state.proxy() as data:
            if document := message.document:
                await message.answer("يرجى ارسال الاسم أولا")
                return
            elif photo := message.photo:
                await message.answer("يرجى ارسال الاسم أولا")
                return
            data['file_name'] = message.text
            open(f"{data['folder']}/files", "a+").close()

        await MergePdf.next()
        await bot.send_message(message.chat.id, "ارسل الملفات وعند الرد على جميع الملفات برسالة 'تم تنزيل الملف' يمكنك ارسل أو ضعط دمج", reply_markup=custom_markup(["دمج", "الغاء الدمج"]))
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "MergePdf_get_file_name", e)


async def MergePdf_cancel_handler(message, state):
    try:
        async with state.proxy() as data:
            shutil.rmtree(data['folder'])
            await message.reply("تم الغاء الدمج وحذف الملفات", reply_markup=get_user_markup(message.from_user.id))
        await state.finish()
    except Exception as e:
        async with state.proxy() as data:
            shutil.rmtree(data['folder'])
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "MergePdf_cancel_handler", e)


async def MergePdf_get_files(message, state):
    try:
        async with state.proxy() as data:
            if document := message.document:
                await document.download(
                    destination_file=f"{data['folder']}/{document.file_name}",
                )
                pdf_count = await get_files_count(data['folder'])
                await message.reply(f"تم تنزيل, العدد الكلي للملفات {pdf_count}")
                with open((data['folder']+"/files"), 'a+') as fls:
                    fls.write(f"{data['folder']}/{document.file_name};")
                    fls.close()
    except Exception as e:
        async with state.proxy() as data:
            shutil.rmtree(data['folder'])
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "MergePdf_get_files", e)


async def MergePdf_merge(message, state):
    try:
        async with state.proxy() as data:
            pdf_count = await get_files_count(data['folder'])
            if pdf_count <= 1:
                await message.answer("يرجى ارسال الملفات الحد الادنى 2")
                return
            f = open((data['folder'] + "/files"), 'r')
            file = f.read()
            f.close()
            pdfs = file.split(";")
            pdfs.remove('')
            await bot.send_document(message.chat.id, document=open(merge_pdfs(pdfs, data['folder'], data['file_name']), 'rb'), reply_markup=get_user_markup(message.from_user.id))
            shutil.rmtree(data['folder'])
        await state.finish()
    except Exception as e:
        async with state.proxy() as data:
            shutil.rmtree(data['folder'])
        await state.finish()
        await message.answer("فشل دمج الملفات", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "MergePdf_merge", e)


def reg(dp):
    dp.register_message_handler(
        Imgs2Pdf_cancel_handler, text="الغاء الدمج", state=MergeImages)
    dp.register_message_handler(
        MergePdf_cancel_handler, text="الغاء الدمج", state=MergePdf)
    dp.register_message_handler(MergePdf_ask_file_name, text="دمج ملفات pdf")
    dp.register_message_handler(Imgs2Pdf_file_name, text="تحويل الصور الى pdf")
    dp.register_message_handler(
        Imgs2Pdf_merge_handler, text="دمج", state=MergeImages.temp)
    dp.register_message_handler(
        MergePdf_merge, text="دمج", state=MergePdf.temp)
    dp.register_message_handler(
        Imgs2Pdf_get_images, state=MergeImages.file_name, content_types=ContentTypes.ANY)
    dp.register_message_handler(
        Imgs2Pdf_Imgs_downloader, state=MergeImages.temp, content_types=ContentTypes.ANY)
    dp.register_message_handler(
        MergePdf_get_file_name, state=MergePdf.file_name, content_types=ContentTypes.ANY)
    dp.register_message_handler(
        MergePdf_get_files, state=MergePdf.temp, content_types=ContentTypes.DOCUMENT)
