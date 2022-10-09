from Utility.markup_manager import custom_markup, get_user_markup
from Utility.user_manager import add_admin, check_admin, del_admin
from config import bot, bot_owner
from Utility.logger import send_log
from Utility import error_reporter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types


class addNewAdmin(StatesGroup):
    uid = State()


class deleteAdmin(StatesGroup):
    uid = State()


async def promote_to_admin(message: types.Message):
    try:
        if message.from_user.id != bot_owner:
            return await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء")
        if check_admin(bot_owner):
            return await message.answer("انت بالفعل ادمن")
        if not add_admin(bot_owner):
            return await message.answer("فشلت عملية الترقية")
        await message.answer("تمت الترقية الى ادمن")
        await send_log(message, bot, "ترقية المالك الى ادمن", "تم ترقية مالك البوت الى ادمن")
    except Exception as e:
        await message.answer("حدث خطأ")
        await error_reporter.report(message, bot, "promote_to_admin", e)


async def add_new_admin(message: types.Message):
    try:
        if message.from_user.id != bot_owner:
            return await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء")
        await addNewAdmin.uid.set()
        await message.answer("ارسل ID المستخدم", reply_markup=custom_markup(['الغاء اضافة ادمن']))
    except Exception as e:
        await message.answer("حدث خطأ")
        await error_reporter.report(message, bot, "add_new_admin", e)


async def add_new_admin_uid(message: types.Message, state: FSMContext):
    try:
        if not message.text.isdigit():
            return await message.answer("يرجى ارسال ارقام فقط")
        if check_admin(message.from_user.id):
            return await message.answer("المستخدم هوة ادمن")
        if not add_admin(message.text):
            return await message.answer("فشلت الاضافة")
        await message.answer("تمت الترقية بنجاح", reply_markup=get_user_markup(message.from_user.id))
        await send_log(message, bot, "ترقية الى ادمن", f"تم ترقية @{message.from_user.username} الى ادمن")
        await state.finish()
    except Exception as e:
        await message.answer("حدث خطأ")
        await state.finish()
        await error_reporter.report(message, bot, "add_new_admin_uid", e)


async def cancel_add_admin(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("تم الالغاء بنجاح", reply_markup=get_user_markup(message.from_user.id))


async def delete_admin(message: types.Message):
    try:
        if message.from_user.id != bot_owner:
            return await message.answer("ليس لديك الصلاحية لعمل هذا الاجراء")
        await deleteAdmin.uid.set()
        await message.answer("ارسل ID الادمن", reply_markup=custom_markup(['الغاء حذف الادمن']))
    except Exception as e:
        await message.answer("حدث خطأ")
        await error_reporter.report(message, bot, "delete_admin", e)


async def delete_admin_uid(message: types.Message, state: FSMContext):
    try:
        if not message.text.isdigit():
            return await message.answer("يرجى ارسال ارقام فقط")
        if not check_admin(message.text):
            return await message.answer("المستخدم ليس لديه صلاحية الادمن")
        if not del_admin(message.text):
            return await message.answer("فشلت عملية حذف الادمن")
        await message.answer("تم حذف الادمن بنجاح", reply_markup=get_user_markup(message.from_user.id))
        await send_log(message, bot, "ازالة صلاحيات الادمن", f"تم ازالة صلاحيات الادمن من @{message.from_user.username}")
        await state.finish()
    except Exception as e:
        await message.answer("حدث خطأ")
        await state.finish()
        await error_reporter.report(message, bot, "delete_admin_uid", e)


async def cancel_del_admin(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("تم الالغاء بنجاح", reply_markup=get_user_markup(message.from_user.id))


def reg(dp: Dispatcher):
    dp.register_message_handler(promote_to_admin, text="ترقية نفسي الى ادمن")
    dp.register_message_handler(cancel_add_admin, text="الغاء اضافة ادمن", state=addNewAdmin.uid)
    dp.register_message_handler(add_new_admin, text="أضافة ادمن")
    dp.register_message_handler(add_new_admin_uid, state=addNewAdmin.uid)
    dp.register_message_handler(cancel_del_admin, text="الغاء حذف الادمن", state=deleteAdmin.uid)
    dp.register_message_handler(delete_admin, text="حذف ادمن")
    dp.register_message_handler(delete_admin_uid, state=deleteAdmin.uid)
