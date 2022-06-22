from aiogram import types
from cmds.user_manager import check_admin, get_manager_stage, check_user_exist

def get_user_markup(uid):
	main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	if check_user_exist(uid) == True:
		main_markup.add("الكتب 📚", "عرض الواجبات 📃")
		# main_markup.add("الصور 📷")
		main_markup.add("أدوات 🧰", "معلوماتي ❓")
		# main_markup.add("ضغط ملف pdf (تقليل حجم)")
		if get_manager_stage(uid) != False:
			main_markup.add("عرض صلاحيات المشرف 💂")
		if check_admin(uid) == True:
			main_markup.add("عرض صلاحيات الادمن 👮")
	else:
		main_markup.add("اختيار المرحلة")
	main_markup.add("أغلاق ❌")
	return main_markup

def admin_markup():
	admin_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	admin_markup.add("اضافة مشرف 💂")
	admin_markup.add("حذف مشرف 💂")
	admin_markup.add("أرسال اعلان للجميع 📢")
	admin_markup.add("عرض جميع المستخدمين 📋")
	admin_markup.add("الرجوع للقائمة الرئيسية 🏠")
	return admin_markup

def manager_markup():
	man_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	man_markup.add("اضافة واجب 📝")
	man_markup.add("حذف واجب 📝")
	man_markup.add("أرسال اعلان 📢")
	man_markup.add("اضافة كتاب 📕")
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
	custom.add("الرجوع للقائمة الرئيسية 🏠")
	return custom