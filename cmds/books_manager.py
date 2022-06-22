import yaml 
import asyncio


async def add_file(stage, name, path):
	with open("storage/links.yml", 'r') as l:
		link = yaml.safe_load(l)
		link[stage]["book_name"].append(name)
		link[stage]["book_path"].append(path)

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
		files_list.append(file_name)

	return files_list

def del_file(stage, name, path):
	with open("storage/links.yml", 'r') as l:
		link = yaml.safe_load(l)
		link[stage]["book_name"].remove(name)
		link[stage]["book_path"].remove(path)
	if link:
		with open("storage/links.yml", 'w') as wd:
			yaml.safe_dump(link, wd)
	return True
