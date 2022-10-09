from Utility.user_manager import check_admin, check_user_stage, get_manager_stage

stage_translate = {
	"stage1": "مرحلة اولى",
	"stage2": "مرحلة ثانية",
	"stage3": "مرحلة ثالثة",
	"stage4": "مرحلة رابعة",
}

def myInfo(message):
	if check_admin(message.from_user.id) == True:
		state = "مسؤول"
	elif get_manager_stage(message.from_user.id) == "stage1":
		state = "مشرف مرحلة اولى"
	elif get_manager_stage(message.from_user.id) == "stage2":
		state = "مشرف مرحلة ثانية"
	elif get_manager_stage(message.from_user.id) == "stage3":
		state = "مشرف مرحلة ثالثة"
	elif get_manager_stage(message.from_user.id) == "Stage4":
		state = "مشرف مرحلة رابعة"
	else:
		state = f"طالب"
	return f"""
الاسم: {message.from_user.full_name}
الأي دي: {message.from_user.id}
الحالة: {state}
المرحلة: {stage_translate[check_user_stage(message.from_user.id)]}
	"""
