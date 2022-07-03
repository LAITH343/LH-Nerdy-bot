import sqlite3
from openpyxl import load_workbook
from datetime import date


def get_bot_users():
    wb = load_workbook("sources/users_sheet.xlsx")
    us = wb.active
    n = 2
    db = sqlite3.connect("storage/users.db")
    c = db.cursor()
    c.execute("SELECT id, username FROM users_info WHERE stage= 'stage1'")
    ids = c.fetchall()
    for i in ids:
        us[f"A{n}"] = f"{int(i[0])} {i[1]}"
        n += 1
    us["F3"] = f"=COUNTA(A2:A{n-1})"
    c.execute("SELECT id, username FROM users_info WHERE stage= 'stage2'")
    ids = c.fetchall()
    n = 2
    for i in ids:
        us[f"B{n}"] = f"{int(i[0])} {i[1]}"
        n += 1
    us["G3"] = f"=COUNTA(B2:B{n-1})"
    wb.save("/home/laith/Desktop/test.xlsx")
    c.execute("SELECT id, username FROM users_info WHERE stage= 'stage3'")
    ids = c.fetchall()
    n = 2
    for i in ids:
        us[f"C{n}"] = f"{int(i[0])} {i[1]}"
        n += 1
    us["H3"] = f"=COUNTA(C2:C{n-1})"
    c.execute("SELECT id, username FROM users_info WHERE stage= 'stage4'")
    ids = c.fetchall()
    n = 2
    for i in ids:
        us[f"D{n}"] = f"{int(i[0])} {i[1]}"
        n += 1
    us["I3"] = f"=COUNTA(D2:D{n-1})"
    output_path = f"cache/{date.today()}.xlsx"
    wb.save(output_path)
    return output_path
