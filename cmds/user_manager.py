import sqlite3
# table users_info
# (id TEXT, name TEXT, username TEXT, stage TEXT, disable TEXT, manager TEXT, admin TEXT)

def add_admin(uid):
	db = sqlite3.connect("storage/users.db")
	c = db.cursor()
	c.execute("Update users_info set admin=? WHERE id=?", ("True", str(uid),))
	db.commit()
	db.close()
	return True


def check_admin(uid):
	db = sqlite3.connect("storage/users.db")
	c = db.cursor()
	c.execute("SELECT admin FROM users_info WHERE admin=? AND id=?", ("True", str(uid),))
	check = c.fetchone()
	if check != None:
		return True
	else:
		return False
	db.close()

def check_user_exist(uid):
	db = sqlite3.connect("storage/users.db")
	c = db.cursor()
	c.execute("SELECT id FROM users_info WHERE id=?", (str(uid),))
	check = c.fetchone()
	if check != None:
		return True
	else:
		return False
	db.close()

def check_user_stage(uid):
	db = sqlite3.connect("storage/users.db")
	c = db.cursor()
	c.execute("SELECT stage FROM users_info WHERE id=?", (str(uid),))
	stage = c.fetchone()
	if stage != None:
		return stage[0]
	else:
		return False
	db.close()


def get_manager_stage(uid):
	db = sqlite3.connect("storage/users.db")
	c = db.cursor()
	c.execute("SELECT stage FROM users_info WHERE id=? AND manager=?", (str(uid), "True",))
	stage = c.fetchone()
	if stage != None:
		return stage[0]
	else:
		return False
	db.close()



def add_user(stage, uid, name, username):
	db = sqlite3.connect("storage/users.db")
	c = db.cursor()
	c.execute("INSERT INTO users_info VALUES (?, ?, ?, ?, ?, ?, ?)", (str(uid), name, username, stage, "False", "False", "False"))
	db.commit()
	db.close()
	return True

def del_user(uid):
	db = sqlite3.connect("storage/users.db")
	c = db.cursor()
	c.execute(f"DELETE FROM users_info WHERE id=?", (uid,))
	db.commit()
	db.close()
	return True

def add_manager(uid):
	db = sqlite3.connect("storage/users.db")
	c = db.cursor()
	c.execute("SELECT id FROM users_info WHERE id=?", (str(uid),))
	stage = c.fetchone()
	if stage != None:
		c.execute("Update users_info set manager=? WHERE id=?", ("True", uid))
		db.commit()
		return True
	else:
		return False
	db.close()

def del_manager(uid):
	db = sqlite3.connect("storage/users.db")
	c = db.cursor()
	c.execute("Update users_info set manager=? WHERE id=?", ("False", uid))
	db.commit()
	db.close()
	return True

def get_users_uid():
	db = sqlite3.connect("storage/users.db")
	c = db.cursor()
	c.execute("SELECT id FROM users_info")
	ids = c.fetchall()
	ul = []
	for id in ids:
		ul.append(id[0])
	db.close()
	return ul

def get_all_usernames():
	db = sqlite3.connect("storage/users.db")
	c = db.cursor()
	c.execute("SELECT username FROM users_info")
	users_name = c.fetchall()
	userlist = []
	for user in users_name:
		userlist.append(user[0])
	db.close()
	return userlist

def get_users_uid_by_stage(stage):
	db = sqlite3.connect("storage/users.db")
	c = db.cursor()
	c.execute("SELECT id FROM users_info WHERE stage=?", (stage,))
	ids = c.fetchall()
	ulbystage = []
	for id in ids:
		ulbystage.append(id[0])
	db.close()
	return ulbystage
