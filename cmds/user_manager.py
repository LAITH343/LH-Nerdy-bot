import sqlite3
import os
# table users_info
# (id TEXT, name TEXT, username TEXT, stage TEXT, disable TEXT, manager TEXT, admin TEXT)
from config import bot_owner

if not os.path.exists("storage/users.db"):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("CREATE TABLE users_info (id TEXT, name TEXT, username TEXT, stage TEXT, disable TEXT, manager TEXT, admin TEXT)")
    c.execute("CREATE TABLE ignore_list (id TEXT)")
    db.commit()
    c.execute("INSERT INTO users_info VALUES (?, ?, ?, ?, ?, ?, ?)", (str(bot_owner), "notset", "notset", "stage1", "False", "False", "True"))
    db.commit()
    db.close()


def ignore_user(uid):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("INSERT INTO ignore_list VALUES (?)", (str(uid),))
    db.commit()
    db.close()
    return True


def unignore_user(uid):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("DELETE FROM ignore_list WHERE id=?", (str(uid),))
    db.commit()
    db.close()
    return True


def get_ignored_users():
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("SELECT id FROM ignore_list")
    users = c.fetchall()
    users_list = []
    if users is not None:
        for u in users:
            users_list.append(u[0])
        db.close()
        return users_list
    else:
        db.close()
        return False


def add_admin(uid):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("Update users_info set admin=? WHERE id=?", ("True", str(uid),))
    db.commit()
    db.close()
    return True


def del_admin(uid):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("Update users_info set admin=? WHERE id=?", ("False", str(uid),))
    db.commit()
    db.close()
    return True


def check_admin(uid):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("SELECT admin FROM users_info WHERE admin=? AND id=?", ("True", str(uid),))
    check = c.fetchone()
    if check is not None:
        db.close()
        return True
    else:
        db.close()
        return False


def check_user_exist(uid):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("SELECT id FROM users_info WHERE id=?", (str(uid),))
    check = c.fetchone()
    if check is not None:
        db.close()
        return True
    else:
        db.close()
        return False


def check_user_stage(uid):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("SELECT stage FROM users_info WHERE id=?", (str(uid),))
    stage = c.fetchone()
    if stage is not None:
        db.close()
        return stage[0]
    else:
        db.close()
        return False


def get_manager_stage(uid):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("SELECT stage FROM users_info WHERE id=? AND manager=?", (str(uid), "True",))
    stage = c.fetchone()
    if stage is not None:
        db.close()
        return stage[0]
    else:
        db.close()
        return False


def add_user(stage, uid, name, username):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("INSERT INTO users_info VALUES (?, ?, ?, ?, ?, ?, ?)", (str(uid), name, username, stage, "False", "False", "False"))
    db.commit()
    db.close()
    unignore_user(uid)
    return True


def del_user(uid, stage):
    if int(uid) == int(bot_owner):
        return False
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute(f"DELETE FROM users_info WHERE id=? AND stage=?", (uid, stage))
    db.commit()
    db.close()
    return True


def add_manager(uid):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("SELECT id FROM users_info WHERE id=?", (str(uid),))
    stage = c.fetchone()
    if stage is not None:
        c.execute("Update users_info set manager=? WHERE id=?", ("True", uid))
        db.commit()
        db.close()
        return True
    else:
        db.close()
        return False


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


async def get_all_usernames():
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("SELECT * FROM users_info")
    users_name = c.fetchall()
    userlist = []
    translate = {
        "stage1": "اولى",
        "stage2": "ثانية",
        "stage3": "ثالثة",
        "stage4": "رابعة",
        "False": "لا",
        "True": "نعم"
    }
    for i in users_name:
        userlist.append(f"""
الأي دي [{i[0]}] 
الاسم [{i[1]}] 
اليوزر [@{i[2]}] 
المرحلة [{translate[i[3]]}] 
محضور [{translate[i[4]]}] 
مشرف [{translate[i[5]]}] 
ادمن [{translate[i[6]]}]
""")
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


def check_user_not_req(uid):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("SELECT name, username FROM users_info WHERE name=? AND username=? AND id=?", ("notset", "notset", str(uid),))
    ids = c.fetchone()
    if ids is not None:
        db.close()
        return True
    else:
        db.close()
        return False


def update_user_info(uid, name, username):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("Update users_info set name=?, username=? WHERE id=?", (name, username, str(uid)))
    db.commit()
    db.close()
    return True


def get_user_username(uid):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("SELECT username FROM users_info WHERE id=?", (str(uid),))
    username = c.fetchone()
    if username is not None:
        db.close()
        return username[0]
    else:
        db.close()
        return False


def check_username_changed(uid, user_name):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("SELECT username FROM users_info WHERE id=? AND (manager='True' OR admin='True')", (str(uid),))
    username = c.fetchone()
    if username is not None:
        if username[0] != user_name:
            db.close()
            return True
        else:
            db.close()
            return False
    else:
        db.close()
        return False


def change_admin_stage(uid, stage):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("Update users_info set stage=? WHERE id=? AND admin=?", (stage, str(uid), "True"))
    db.commit()
    db.close()
    return True

def get_admin_stage(uid):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("SELECT stage FROM users_info WHERE id=? AND admin='True'", (str(uid),))
    stage = c.fetchone()
    if stage is not None:
        db.close()
        return stage[0]
    else:
        db.close()
        return False

def get_user_id(username: str):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("SELECT id FROM users_info WHERE username=?", (username,))
    uid = c.fetchone()
    if uid is not None:
        db.close()
        return uid[0]
    else:
        db.close()
        return False

def get_user_full_info(uid):
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("SELECT * FROM users_info WHERE id=?", (str(uid),))
    users_name = c.fetchone()
    userlist = []
    # 0: id, 1: name, 2: username, 3: stage, 4: Is manager, 5: Is admin 
    return [users_name[0], users_name[1], users_name[2], users_name[3], users_name[5], users_name[6]]