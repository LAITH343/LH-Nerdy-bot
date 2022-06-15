from cmds.user_check import check

def myInfo(message):
	return f"""
Name: {message.from_user.full_name}
ID: {message.from_user.id}
Admin: {check(message.from_user.id)}
	"""