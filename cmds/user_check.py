import yaml

with open('config.yml', 'r') as ucfg:
	cfg = yaml.safe_load(ucfg)
	user = cfg['users']['admin']

def check(uid):
	if uid in user:
		return True
	else:
		return False