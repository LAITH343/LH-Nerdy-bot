from cmds.user_manager import check_admin

def myInfo(message):
	return f"""
Name: {message.from_user.full_name}
ID: {message.from_user.id}
Admin: {check_admin(message.from_user.id)}
	"""