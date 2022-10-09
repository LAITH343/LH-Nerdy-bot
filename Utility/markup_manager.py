from aiogram import types
from Utility.user_manager import check_admin, get_manager_stage, check_user_exist
from config import bot_owner


def get_user_markup(uid):
    main_markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, selective=True)
    if check_user_exist(uid):
        main_markup.add("الأدوات 🧰", "الواجبات 📃")
        main_markup.add("الملفات 📎", "الكتب 📚")
        main_markup.add("معلوماتي ❓", )
        if get_manager_stage(uid):
            main_markup.add("صلاحيات المشرف 💂")
        if check_admin(uid):
            main_markup.add("صلاحيات الادمن 👮")
        if uid == bot_owner:
            main_markup.add("صلاحيات مالك البوت")
    else:
        pass
    main_markup.add("أغلاق القائمة ❌")
    return main_markup


def admin_markup():
    admin_markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, selective=True)
    admin_markup.add("تغيير المرحلة 🔄", "أرسال اعلان للجميع 📢")
    admin_markup.add("ادارة الطلاب")
    admin_markup.add("الرجوع للقائمة الرئيسية 🏠")
    return admin_markup


def manager_markup():
    man_markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, selective=True)
    man_markup.add("الواجبات و الملفات")
    man_markup.add("أدارة الطلاب")
    man_markup.add("أرسال اعلان 📢")
    man_markup.add("الرجوع للقائمة الرئيسية 🏠")
    return man_markup


def custom_markup(options: list):
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for option in options:
        custom.add(option)
    return custom


def books_markup(options: list):
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for option in options:
        custom.add(option)
    custom.add("الرجوع للقائمة الرئيسية")
    return custom


def del_books_markup(options: list):
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for option in options:
        custom.add(option)
    if not options:
        custom.add("الرجوع للقائمة الرئيسية 🏠")
    else:
        custom.add("الغاء الحذف")
    return custom


def extra_file_markup(options: list):
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for option in options:
        custom.add(option)
    custom.add("الرجوع للقائمة الرئيسية")
    return custom


def del_extra_file_markup(options: list):
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for option in options:
        custom.add(option)
    if not options:
        custom.add("الرجوع للقائمة الرئيسية 🏠")
    else:
        custom.add("الغاء حذف الملف")
    return custom


def manage_users_markup():
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    custom.add("أضافة طالب", "حذف طالب")
    custom.add("عرض معلومات طالب")
    custom.add("الرجوع الى صلاحيات المشرف")
    return custom


def manager_hwandfiles_markup():
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    custom.add("اضافة واجب 📝", "حذف واجب 📝")
    custom.add("اضافة كتاب 📕", "حذف كتاب ❌")
    custom.add("اضافة ملف 📎", "حذف ملف ❌")
    custom.add("الرجوع الى صلاحيات المشرف")
    return custom


def admin_user_mangment():
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    custom.add("اضافة مشرف 💂", "حذف مشرف 💂")
    custom.add("أضافة طالب جديد", "حّذف طالب")
    custom.add("عرض معلومات مفصلة عن طالب")
    custom.add("عرض جميع المستخدمين 📋")
    custom.add("الرجوع الى صلاحيات الادمن")
    return custom


def owner_markup():
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    if not check_admin(bot_owner):
        custom.add("ترقية نفسي الى ادمن")
    custom.add("أضافة ادمن")
    custom.add("حذف ادمن")
    custom.add("الرجوع للقائمة الرئيسية 🏠")
    return custom
