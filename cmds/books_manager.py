import os
import sqlite3
# books (stage TEXT, book_name TEXT, book_path TEXT)
# files (stage TEXT, file_name TEXT, file_path TEXT)
try:
	db = sqlite3.connect("storage/main_storage.db")
	c = db.cursor()
	c.execute("CREATE TABLE books (stage TEXT, book_name TEXT, book_path TEXT)")
	c.execute("CREATE TABLE files (stage TEXT, file_name TEXT, file_path TEXT)")
	db.commit()
	db.close()
except:
	pass


async def add_file(stage, name, path):
	try:
		db = sqlite3.connect("storage/main_storage.db")
		c = db.cursor()
		c.execute("INSERT INTO books VALUES (?, ?, ?)", (stage, name, path))
		db.commit()
		db.close()
		return True
	except:
		return False


async def add_extra_file(stage, name, path):
	try:
		db = sqlite3.connect("storage/main_storage.db")
		c = db.cursor()
		c.execute("INSERT INTO files VALUES (?, ?, ?)", (stage, name, path))
		db.commit()
		db.close()
		return True
	except:
		return False


def get_files_list(stage):
	db = sqlite3.connect("storage/main_storage.db")
	c = db.cursor()
	c.execute("SELECT book_name FROM books WHERE stage=?", (stage,))
	file_name = c.fetchall()
	files_list = []
	for file in file_name:
		files_list.append(file[0])
	db.close()
	return files_list


def get_extra_files_list(stage):
	db = sqlite3.connect("storage/main_storage.db")
	c = db.cursor()
	c.execute("SELECT file_name FROM files WHERE stage=?", (stage,))
	file_name = c.fetchall()
	files_list = []
	for file in file_name:
		files_list.append(file[0])
	db.close()
	return files_list


async def del_file(stage, name):
	db = sqlite3.connect("storage/main_storage.db")
	c = db.cursor()
	c.execute("SELECT book_path FROM books WHERE stage=? AND book_name=?", (stage, name))
	file = c.fetchone()
	os.remove(file[0])
	c.execute("DELETE FROM books WHERE stage=? AND book_name=?", (stage, name))
	db.commit()
	db.close()
	return True


async def del_extra_file(stage, name):
	db = sqlite3.connect("storage/main_storage.db")
	c = db.cursor()
	c.execute("SELECT file_path FROM files WHERE stage=? AND file_name=?", (stage, name))
	file = c.fetchone()
	os.system(file[0])
	c.execute("DELETE FROM files WHERE stage=? AND file_name=?", (stage, name))
	db.commit()
	db.close()
	return True


def get_file_by_name(stage, name):
	db = sqlite3.connect("storage/main_storage.db")
	c = db.cursor()
	c.execute("SELECT book_path FROM books WHERE stage=? AND book_name=?", (stage, name))
	file_path = c.fetchone()
	db.close()
	return file_path[0]


def get_extra_file_by_name(stage, name):
	db = sqlite3.connect("storage/main_storage.db")
	c = db.cursor()
	c.execute("SELECT file_path FROM files WHERE stage=? AND file_name=?", (stage, name))
	file_path = c.fetchone()
	db.close()
	return file_path[0]
