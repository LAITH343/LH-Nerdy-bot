import asyncio
import random
import string
import os
from aiogram import types
from cmds.user_manager import check_user_exist
from cmds.markup_manager import get_user_markup, custom_markup
from cmds.classes import MergeImages, MergePdf
from cmds.pdf_manager import images_to_pdf, merge_pdfs


async def Imgs2Pdf_file_name(message, state):
	if check_user_exist(message.from_user.id) == False:
	    await message.reply("اختر المرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
	else:
	    await MergeImages.folder.set()
	    randfile = ''.join(random.choice(string.ascii_lowercase) for i in range(20))
	    os.system(f"mkdir cache/{randfile}")
	    async with state.proxy() as data:
	        data['folder'] = f"cache/{randfile}"
	    await MergeImages.next()
	    await message.reply("ماذا تريد ان تسمي الملف؟", reply_markup=custom_markup(["الغاء الدمج"]))

async def Imgs2Pdf_get_images(message, state):
	if check_user_exist(message.from_user.id) == False:
	    await message.reply("اختر المرحلة اولا", reply_markup=get_user_markup(message.from_user.id))
	else:
	    async with state.proxy() as data:
	        data['file_name'] = message.text

	    await MergeImages.next()
	    await message.reply("ارسل الصور وعند الرد على جميع الصور برسالة 'تم تنزيل الملف' يمكنك ارسل أو ضعط دمج", reply_markup=custom_markup(["دمج","الغاء الدمج"]))

async def Imgs2Pdf_cancel_handler(message, state):
	async with state.proxy() as data:
	    os.system(f"rm -rf {data['folder']}")
	    await message.reply("تم الغاء الدمج وحذف الملفات", reply_markup=get_user_markup(message.from_user.id))
	await state.finish()

async def Imgs2Pdf_Imgs_downloader(message, state):
	async with state.proxy() as data:
	    if document := message.document:
	        await document.download(
	            destination_file=f"{data['folder']}/{document.file_name}",
	        )
	        await message.reply("تم تنزيل الملف")
	        with open((data['folder']+"/files"), 'a+') as fls:
	            fls.write(f"{data['folder']}/{document.file_name};")
	            fls.close()

async def Imgs2Pdf_merge_handler(message, state, bot):
	async with state.proxy() as data:
	    f = open((data['folder'] + "/files"), 'r')
	    file = f.read()
	    pdfs = file.split(";")
	    pdfs.remove('')
	    try:
	        await bot.send_message(message.chat.id, "جاري دمج الصور و رفع الملف")
	        await bot.send_document(message.chat.id, document=open(images_to_pdf(pdfs, data['folder'], data['file_name']), 'rb'), reply_markup=get_user_markup(message.from_user.id))
	    except:
	        await message.reply("فشل دمج الملفات")
	    os.system(f"rm -rf {data['folder']}")
	await state.finish()

async def MergePdf_ask_file_name(message, state):
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

async def MergePdf_get_file_name(message, state, bot):
	async with state.proxy() as data:
	    data['file_name'] = message.text

	await MergePdf.next()
	await bot.send_message(message.chat.id, "ارسل الملفات وعند الرد على جميع الملفات برسالة 'تم تنزيل الملف' يمكنك ارسل أو ضعط دمج", reply_markup=custom_markup(["دمج","الغاء الدمج"]))

async def MergePdf_cancel_handler(message, state):
	async with state.proxy() as data:
	    os.system(f"rm -rf {data['folder']}")
	    await message.reply("تم الغاء الدمج وحذف الملفات", reply_markup=get_user_markup(message.from_user.id))
	await state.finish()

async def MergePdf_get_files(message, state):
	async with state.proxy() as data:
	    if document := message.document:
	        await document.download(
	            destination_file=f"{data['folder']}/{document.file_name}",
	        )
	        await message.reply("تم تنزيل الملف")
	        with open((data['folder']+"/files"), 'a+') as fls:
	            fls.write(f"{data['folder']}/{document.file_name};")
	            fls.close()

async def MergePdf_merge(message, state, bot):
	async with state.proxy() as data:
	    f = open((data['folder'] + "/files"), 'r')
	    file = f.read()
	    pdfs = file.split(";")
	    pdfs.remove('')
	    try:
	        await bot.send_document(message.chat.id, document=open(merge_pdfs(pdfs, data['folder'], data['file_name']), 'rb'), reply_markup=get_user_markup(message.from_user.id))
	    except:
	        await message.reply("فشل دمج الملفات")
	        os.system(f"rm -rf {data['folder']}")
	    os.system(f"rm -rf {data['folder']}")
	await state.finish()