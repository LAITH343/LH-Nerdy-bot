import yaml 

with open("links.yml", 'r') as l:
	link = yaml.safe_load(l)

def links(name):
	return link[name]