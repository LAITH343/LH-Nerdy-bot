import yaml 
import asyncio
from os import system


async def add_file(stage, name, path):
	with open("storage/links.yml", 'r') as l:
		link = yaml.safe_load(l)
		link[stage]["book_name"].append(name)
		link[stage]["book_path"].append(path)

	if link:
		with open('storage/links.yml', 'w') as w:
			yaml.safe_dump(link, w)
	return True

async def add_extra_file(stage, name, path):
	with open("storage/links.yml", 'r') as l:
		link = yaml.safe_load(l)
		link[stage]["extra_file_name"].append(name)
		link[stage]["extra_file_path"].append(path)

	if link:
		with open('storage/links.yml', 'w') as w:
			yaml.safe_dump(link, w)
	return True

def get_files_list(stage):
	with open("storage/links.yml", 'r') as l:
		link = yaml.safe_load(l)
		file_name = link[stage]["book_name"]
	
	files_list = []	
	for file in file_name:
		files_list.append(file[0:])

	return files_list

def get_extra_files_list(stage):
	with open("storage/links.yml", 'r') as l:
		link = yaml.safe_load(l)
		file_name = link[stage]["extra_file_name"]
	
	files_list = []	
	for file in file_name:
		files_list.append(file[0:])

	return files_list

async def del_file(stage, name):
	with open("storage/links.yml", 'r') as l:
		link = yaml.safe_load(l)
		index = link[stage]["book_name"].index(name)
		file_be_del = link[stage]["book_path"][index]
		link[stage]["book_name"].pop(index)
		link[stage]["book_path"].pop(index)
	if link:
		system(f"rm -f {file_be_del}")
		with open("storage/links.yml", 'w') as wd:
			yaml.safe_dump(link, wd)
	return True

async def del_extra_file(stage, name):
	with open("storage/links.yml", 'r') as l:
		link = yaml.safe_load(l)
		index = link[stage]["extra_file_name"].index(name)
		file_be_del = link[stage]["extra_file_path"][index]
		link[stage]["extra_file_name"].pop(index)
		link[stage]["extra_file_path"].pop(index)
	if link:
		system(f"rm -f {file_be_del}")
		with open("storage/links.yml", 'w') as wd:
			yaml.safe_dump(link, wd)
	return True

def get_file_by_name(stage, name):
	with open("storage/links.yml", 'r') as links:
		cfg = yaml.safe_load(links)
		index = cfg[stage]["book_name"].index(name)
		file_path = cfg[stage]["book_path"][index]
	
	return file_path

def get_extra_file_by_name(stage, name):
	with open("storage/links.yml", 'r') as links:
		cfg = yaml.safe_load(links)
		index = cfg[stage]["extra_file_name"].index(name)
		file_path = cfg[stage]["extra_file_path"][index]
	
	return file_path