import yaml 

with open("storage/links.yml", 'r') as l:
	link = yaml.safe_load(l)

def links(name):
	return link[name]