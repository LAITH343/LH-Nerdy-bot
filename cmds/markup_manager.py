from aiogram import types
from cmds.user_manager import check_admin, get_manager_stage, check_user_exist


# create main menu 
main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
main_markup.add("عرض الواجبات 📃")
main_markup.add("ملازم 📚")
main_markup.add("الصور 📷")
main_markup.add("معلوماتي ❓")
main_markup.add("أغلاق ❌")

# create admin main menu 
admin_main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
admin_main_markup.add("عرض الواجبات 📃")
admin_main_markup.add("ملازم 📚")
admin_main_markup.add("الصور 📷")
admin_main_markup.add("معلوماتي ❓")
admin_main_markup.add("اضافة مشرف 💂")
admin_main_markup.add("حذف مشرف 💂")
admin_main_markup.add("أرسال اعلان للجميع 📢")
admin_main_markup.add("أغلاق ❌")

# create manager user main menu 
man_main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
man_main_markup.add("عرض الواجبات 📃")
man_main_markup.add("اضافة واجب 📝")
man_main_markup.add("حذف واجب 📝")
man_main_markup.add("أرسال اعلان 📢")
man_main_markup.add("ملازم 📚")
man_main_markup.add("الصور 📷")
man_main_markup.add("معلوماتي ❓")
man_main_markup.add("أغلاق ❌")

# create new user main menu 
new_user_main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
new_user_main_markup.add("اختيار المرحلة")
new_user_main_markup.add("أغلاق ❌")


def get_user_markup(uid):
	if check_admin(uid) == True:
		return admin_main_markup
	elif get_manager_stage(uid) != False:
		return man_main_markup
	elif check_user_exist(uid) == True:
		return main_markup
	else:
		return new_user_main_markup
