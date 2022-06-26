import asyncio
import random
import string
import os
from aiogram import types
from cmds.user_manager import check_user_exist
from cmds.markup_manager import get_user_markup, custom_markup
from cmds.classes import MergeImages, MergePdf
from cmds.pdf_manager import images_to_pdf, merge_pdfs
from cmds import error_reporter


async def Imgs2Pdf_file_name(message, state, bot):
    if check_user_exist(message.from_user.id) == False:
        await message.reply("اختر المرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
    else:
        try:
            await MergeImages.folder.set()
            randfile = ''.join(random.choice(string.ascii_lowercase) for i in range(20))
            os.system(f"mkdir cache/{randfile}")
            async with state.proxy() as data:
                data['folder'] = f"cache/{randfile}"
            await MergeImages.next()
            await message.reply("ماذا تريد ان تسمي الملف؟", reply_markup=custom_markup(["الغاء الدمج"]))
        except Exception as e:
            async with state.proxy() as data:
                os.system(f"rm -rf {data['folder']}")
            await state.finish()
            await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
            await error_reporter.report(message, bot, "Imgs2Pdf_file_name", e)

async def Imgs2Pdf_get_images(message, state, bot):
    if check_user_exist(message.from_user.id) == False:
        await message.reply("اختر المرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
    else:
        try:
            async with state.proxy() as data:
                data['file_name'] = message.text

            await MergeImages.next()
            await message.reply("ارسل الصور وعند الرد على جميع الصور برسالة 'تم تنزيل الملف' يمكنك ارسل أو ضعط دمج", reply_markup=custom_markup(["دمج","الغاء الدمج"]))
        except Exception as e:
            async with state.proxy() as data:
                os.system(f"rm -rf {data['folder']}")
            await state.finish()
            await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
            await error_reporter.report(message, bot, "Imgs2Pdf_get_images", e)

async def Imgs2Pdf_cancel_handler(message, state, bot):
    try:
        async with state.proxy() as data:
            os.system(f"rm -rf {data['folder']}")
            await message.reply("تم الغاء الدمج وحذف الملفات", reply_markup=get_user_markup(message.from_user.id))
        await state.finish()
    except Exception as e:
        async with state.proxy() as data:
            os.system(f"rm -rf {data['folder']}")
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Imgs2Pdf_cancel_handler", e)

async def Imgs2Pdf_Imgs_downloader(message, state, bot):
    try:
        async with state.proxy() as data:
            if document := message.document:
                await document.download(destination_file=f"{data['folder']}/{document.file_name}",)
                await message.reply("تم تنزيل الملف")
                with open((data['folder'] + "/files"), 'a+') as fls:
                    fls.write(f"{data['folder']}/{document.file_name};")
                    fls.close()

            elif photo := message.photo:
                rand_name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
                await photo[-1].download(destination_file=f"{data['folder']}/{rand_name}",)
                await message.reply("تم تنزيل الملف")
                with open((data['folder'] + "/files"), 'a+') as fls:
                    fls.write(f"{data['folder']}/{rand_name};")
                    fls.close()
            else:
                await message.answer("الرجاء ارسال صورة")
    except Exception as e:
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Imgs2Pdf_Imgs_downloader", e)


async def Imgs2Pdf_merge_handler(message, state, bot):
    try:
        async with state.proxy() as data:
            f = open((data['folder'] + "/files"), 'r')
            file = f.read()
            pdfs = file.split(";")
            pdfs.remove('')
            await bot.send_message(message.chat.id, "جاري دمج الصور و رفع الملف")
            await bot.send_document(message.chat.id, document=open(images_to_pdf(pdfs, data['folder'], data['file_name']), 'rb'), reply_markup=get_user_markup(message.from_user.id))
            os.system(f"rm -rf {data['folder']}")
        await state.finish()
    except Exception as e:
        async with state.proxy() as data:
            os.system(f"rm -rf {data['folder']}")
        await state.finish()
        await message.answer("فشل دمج الملفات", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "Imgs2Pdf_merge_handler", e)

async def MergePdf_ask_file_name(message, state, bot):
    try:
        if check_user_exist(message.from_user.id) == False:
            await message.reply("اختر المرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
        else:
            await MergePdf.folder.set()
            randfile = ''.join(random.choice(string.ascii_lowercase) for i in range(20))
            os.system(f"mkdir cache/{randfile}")
            async with state.proxy() as data:
                data['folder'] = f"cache/{randfile}"
            await MergePdf.next()
            await message.reply("ماذا تريد ان تسمي الملف؟", reply_markup=custom_markup(["الغاء الدمج"]))
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "MergePdf_ask_file_name", e)

async def MergePdf_get_file_name(message, state, bot):
    try:
        async with state.proxy() as data:
            data['file_name'] = message.text

        await MergePdf.next()
        await bot.send_message(message.chat.id, "ارسل الملفات وعند الرد على جميع الملفات برسالة 'تم تنزيل الملف' يمكنك ارسل أو ضعط دمج", reply_markup=custom_markup(["دمج","الغاء الدمج"]))
    except Exception as e:
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "MergePdf_get_file_name", e)

async def MergePdf_cancel_handler(message, state, bot):
    try:
        async with state.proxy() as data:
            os.system(f"rm -rf {data['folder']}")
            await message.reply("تم الغاء الدمج وحذف الملفات", reply_markup=get_user_markup(message.from_user.id))
        await state.finish()
    except Exception as e:
        async with state.proxy() as data:
            os.system(f"rm -rf {data['folder']}")
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "MergePdf_cancel_handler", e)

async def MergePdf_get_files(message, state, bot):
    try:
        async with state.proxy() as data:
            if document := message.document:
                await document.download(
                    destination_file=f"{data['folder']}/{document.file_name}",
                )
                await message.reply("تم تنزيل الملف")
                with open((data['folder']+"/files"), 'a+') as fls:
                    fls.write(f"{data['folder']}/{document.file_name};")
                    fls.close()
    except Exception as e:
        async with state.proxy() as data:
            os.system(f"rm -rf {data['folder']}")
        await state.finish()
        await message.answer("حدث خطأ", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "MergePdf_get_files", e)

async def MergePdf_merge(message, state, bot):
    try:
        async with state.proxy() as data:
            f = open((data['folder'] + "/files"), 'r')
            file = f.read()
            pdfs = file.split(";")
            pdfs.remove('')
            await bot.send_document(message.chat.id, document=open(merge_pdfs(pdfs, data['folder'], data['file_name']), 'rb'), reply_markup=get_user_markup(message.from_user.id))
            os.system(f"rm -rf {data['folder']}")
        await state.finish()
    except Exception as e:
        async with state.proxy() as data:
            os.system(f"rm -rf {data['folder']}")
        await state.finish()
        await message.answer("فشل دمج الملفات", reply_markup=get_user_markup(message.from_user.id))
        await error_reporter.report(message, bot, "MergePdf_merge", e)