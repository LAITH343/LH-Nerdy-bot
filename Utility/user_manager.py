# table users_info
# (id TEXT, name TEXT, username TEXT, stage TEXT, disable TEXT, manager TEXT, admin TEXT)
from config import bot_owner, db, c

# if not os.path.exists("storage/users.db"):
c.execute("CREATE TABLE IF NOT EXISTS users_info (id VARCHAR(100), name VARCHAR(100), username VARCHAR(100), stage VARCHAR(100), disable VARCHAR(100), manager VARCHAR(100), admin VARCHAR(100))")
c.execute("CREATE TABLE IF NOT EXISTS ignore_list (id VARCHAR(100))")
db.commit()
c.execute(f"SELECT * FROM users_info where id='{str(bot_owner)}'")
if c.fetchone() is None:
    c.execute(f"INSERT INTO users_info VALUES ('{str(bot_owner)}', 'notset', 'notset', 'stage1', 'False', 'False', 'False')")
db.commit()


def ignore_user(uid):
    c.execute(f"INSERT INTO ignore_list VALUES ('{str(uid)}')")
    db.commit()
    return True


def unignore_user(uid):
    c.execute(f"DELETE FROM ignore_list WHERE id='{str(uid)}'")
    db.commit()
    return True


def get_ignored_users():
    c.execute("SELECT id FROM ignore_list")
    users = c.fetchall()
    users_list = []
    if users is not None:
        for u in users:
            users_list.append(u[0])
        return users_list
    else:
        return False


def add_admin(uid):
    c.execute(f"Update users_info set admin='True' WHERE id='{str(uid)}'")
    db.commit()
    return True


def del_admin(uid):
    c.execute(f"Update users_info set admin='False' WHERE id='{str(uid)}'")
    db.commit()
    return True


def check_admin(uid):
    c.execute(f"SELECT admin FROM users_info WHERE admin='True' AND id='{str(uid)}'")
    check = c.fetchone()
    if check is not None:
        return True
    else:
        return False


def check_user_exist(uid):
    c.execute(f"SELECT id FROM users_info WHERE id='{str(uid)}'")
    check = c.fetchone()
    if check is not None:
        return True
    else:
        return False


def check_user_stage(uid):
    c.execute(f"SELECT stage FROM users_info WHERE id='{str(uid)}'")
    stage = c.fetchone()
    if stage is not None:
        return stage[0]
    else:
        return False


def get_manager_stage(uid):
    c.execute(f"SELECT stage FROM users_info WHERE id='{str(uid)}' AND manager='True'")
    stage = c.fetchone()
    if stage is not None:
        return stage[0]
    else:
        return False


def add_user(stage, uid, name, username):
    c.execute(f"INSERT INTO users_info VALUES ('{str(uid)}', '{name}', '{username}', '{stage}', 'False', 'False', 'False')")
    db.commit()
    unignore_user(uid)
    return True


def del_user(uid, stage):
    if int(uid) == int(bot_owner):
        return False
    c.execute(f"DELETE FROM users_info WHERE id='{uid}' AND stage='{stage}'")
    db.commit()
    return True


def add_manager(uid):
    c.execute(f"SELECT id FROM users_info WHERE id='{str(uid)}'")
    stage = c.fetchone()
    if stage is not None:
        c.execute(f"Update users_info set manager='True' WHERE id='{uid}'")
        db.commit()
        return True
    else:
        return False


def del_manager(uid):
    c.execute(f"Update users_info set manager='False' WHERE id='{uid}'")
    db.commit()
    return True


def get_users_uid():
    c.execute("SELECT id FROM users_info")
    ids = c.fetchall()
    ul = []
    for id in ids:
        ul.append(id[0])
    return ul


async def get_all_usernames():
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
    return userlist


def get_users_uid_by_stage(stage):
    c.execute(f"SELECT id FROM users_info WHERE stage='{stage}'")
    ids = c.fetchall()
    ulbystage = []
    for id in ids:
        ulbystage.append(id[0])
    return ulbystage


def check_user_not_req(uid):
    c.execute(f"SELECT name, username FROM users_info WHERE name='notset' AND username='notset' AND id='{str(uid)}'")
    ids = c.fetchone()
    if ids is not None:
        return True
    else:
        return False


def update_user_info(uid, name, username):
    c.execute(f"Update users_info set name='{name}', username='{username}' WHERE id='{str(uid)}'")
    db.commit()
    return True


def get_user_username(uid):
    c.execute(f"SELECT username FROM users_info WHERE id='{str(uid)}'")
    username = c.fetchone()
    if username is not None:
        return username[0]
    else:
        return False


def check_username_changed(uid, user_name):
    c.execute(f"SELECT username FROM users_info WHERE id='{str(uid)}' AND (manager='True' OR admin='True')")
    username = c.fetchone()
    if username is not None:
        if username[0] != user_name:
            return True
        else:
            return False
    else:
        return False


def change_admin_stage(uid, stage):
    c.execute(f"Update users_info set stage='{stage}' WHERE id='{str(uid)}' AND admin='True'")
    db.commit()
    return True

def get_admin_stage(uid):
    c.execute(f"SELECT stage FROM users_info WHERE id='{str(uid)}' AND admin='True'")
    stage = c.fetchone()
    if stage is not None:
        return stage[0]
    else:
        return False

def get_user_id(username: str):
    c.execute(f"SELECT id FROM users_info WHERE username='{username}'")
    uid = c.fetchone()
    if uid is not None:
        return uid[0]
    else:
        return False

def get_user_full_info(uid):
    c.execute(f"SELECT * FROM users_info WHERE id='{str(uid)}'")
    users_name = c.fetchone()
    userlist = []
    # 0: id, 1: name, 2: username, 3: stage, 4: Is manager, 5: Is admin 
    return [users_name[0], users_name[1], users_name[2], users_name[3], users_name[5], users_name[6]]