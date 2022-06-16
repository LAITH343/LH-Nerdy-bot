import yaml

def check(uid):
	with open('config.yml', 'r') as ucfg:
		cfg = yaml.safe_load(ucfg)
		user = cfg['users']['admin']
	if uid in user:
		return True
	else:
		return False
	cfg.close()

def check_user_exist(uid):
	with open('config.yml', 'r') as ucfg:
		cfg = yaml.safe_load(ucfg)
		stage1 = cfg['users']['stage1']
		stage2 = cfg['users']['stage2']
		stage3 = cfg['users']['stage3']
		stage4 = cfg['users']['stage4']
	if uid in stage1 or stage2 or stage3 or stage4:
		return True
	else:
		return False
	cfg.close()