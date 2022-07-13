import sqlite3

try:
    db = sqlite3.connect("storage/main_storage.db")
    c = db.cursor()
    c.execute("CREATE TABLE hw (stage TEXT, sunday TEXT, monday TEXT, tuesday TEXT, wednesday TEXT, thursday TEXT)")
    db.commit()
    c.execute("INSERT INTO hw VALUES (?, ?, ?, ?, ?, ?)", ("stage1", "لا شيء", "لا شيء", "لا شيء", "لا شيء", "لا شيء"))
    c.execute("INSERT INTO hw VALUES (?, ?, ?, ?, ?, ?)", ("stage2", "لا شيء", "لا شيء", "لا شيء", "لا شيء", "لا شيء"))
    c.execute("INSERT INTO hw VALUES (?, ?, ?, ?, ?, ?)", ("stage3", "لا شيء", "لا شيء", "لا شيء", "لا شيء", "لا شيء"))
    c.execute("INSERT INTO hw VALUES (?, ?, ?, ?, ?, ?)", ("stage4", "لا شيء", "لا شيء", "لا شيء", "لا شيء", "لا شيء"))
    db.commit()
    db.close()
except:
    pass


def add_hw(stage, day, m):
    db = sqlite3.connect("storage/main_storage.db")
    c = db.cursor()
    c.execute(f"Update hw set {day}=? WHERE stage=?", (m, stage))
    db.commit()
    db.close()
    return True


def get_hw(stage, day):
    db = sqlite3.connect("storage/main_storage.db")
    c = db.cursor()
    c.execute(f"SELECT {day} FROM hw WHERE stage=?", (stage,))
    HW = c.fetchone()
    db.close()
    return HW[0]


def get_hw_allweek(stage):
    db = sqlite3.connect("storage/main_storage.db")
    c = db.cursor()
    c.execute("SELECT * FROM hw WHERE stage=?", (stage,))
    hw = c.fetchone()
    week = ""
    keys = [
        "الاحد",
        "الاثنين",
        "الثلاثاء",
        "الاربعاء",
        "الخميس"
    ]
    for i in range(5):
        week += f"---- {keys[i]} ----\n {hw[i+1]}\n"
    return week
