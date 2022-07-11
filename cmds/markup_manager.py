from aiogram import types
from cmds.user_manager import check_admin, get_manager_stage, check_user_exist


def get_user_markup(uid):
	main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	if check_user_exist(uid):
		main_markup.add("معلوماتي ❓", "عرض الواجبات 📃")
		main_markup.add("الملفات 📎", "الكتب 📚")
		main_markup.add("الأدوات 🧰", )
		if get_manager_stage(uid):
			main_markup.add("عرض صلاحيات المشرف 💂")
		if check_admin(uid):
			main_markup.add("عرض صلاحيات الادمن 👮")
	else:
		pass
	main_markup.add("أغلاق ❌")
	return main_markup


def admin_markup():
	admin_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	admin_markup.add("اضافة مشرف 💂", "حذف مشرف 💂")
	admin_markup.add("تغيير المرحلة 🔄")
	admin_markup.add("أرسال اعلان للجميع 📢")
	admin_markup.add("عرض جميع المستخدمين 📋")
	admin_markup.add("الرجوع للقائمة الرئيسية 🏠")
	return admin_markup


def manager_markup():
	man_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	man_markup.add("أضافة طالب", "حذف طالب")
	man_markup.add("اضافة واجب 📝", "حذف واجب 📝")
	man_markup.add("اضافة كتاب 📕", "حذف كتاب ❌")
	man_markup.add("اضافة ملف 📎", "حذف ملف ❌")
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