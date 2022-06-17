from cmds.user_manager import check_admin, check_user_stage_name, check_user_exist, get_manager_stage

def myInfo(message):
	if check_admin(message.from_user.id) == True:
		state = "مسؤول"
	elif get_manager_stage(message.from_user.id) == 1:
		state = "مشرف مرحلة اولى"
	elif get_manager_stage(message.from_user.id) == 2:
		state = "مشرف مرحلة ثانية"
	elif get_manager_stage(message.from_user.id) == 3:
		state = "مشرف مرحلة ثالثة"
	elif get_manager_stage(message.from_user.id) == 4:
		state = "مشرف مرحلة رابعة"
	else:
		state = f"طالب"
	return f"""
الاسم: {message.from_user.full_name}
الأي دي: {message.from_user.id}
الحالة: {state}
المرحلة: {check_user_stage_name(message.from_user.id)}
	"""
