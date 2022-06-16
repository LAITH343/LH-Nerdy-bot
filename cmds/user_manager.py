import yaml

def check_admin(uid):
	with open('storage/users_info.yml', 'r') as ucfg:
		cfg = yaml.safe_load(ucfg)
		user = cfg['users']['admin']
	if uid in user:
		return True
	else:
		return False
	cfg.close()

def check_user_exist(uid):
	with open('storage/users_info.yml', 'r') as ucfg:
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

def check_user_stage(uid):
	with open('storage/users_info.yml', 'r') as ucfg:
		cfg = yaml.safe_load(ucfg)
		stage1 = cfg['users']['stage1']
		stage2 = cfg['users']['stage2']
		stage3 = cfg['users']['stage3']
		stage4 = cfg['users']['stage4']
	if uid in stage1:
		return "1"
	elif uid in stage2:
		return "2"
	elif uid in stage3:
		return "3"
	elif uid in stage4:
		return "4"
	else:
		return False
	cfg.close()

def add_user(stage, uid):
	with open('storage/users_info.yml', 'r') as ucfg:
		cfg = yaml.safe_load(ucfg)
		cfg['users'][stage].append(uid)
	if cfg:
		with open('storage/users_info.yml', 'w') as ucfg:
			yaml.safe_dump(cfg, ucfg)
	return True

def del_user(stage, uid):
	with open('storage/users_info.yml', 'r') as ucfg:
		cfg = yaml.safe_load(ucfg)
		cfg['users'][stage].remove(uid)
	if cfg:
		with open('storage/users_info.yml', 'w') as ucfg:
			yaml.safe_dump(cfg, ucfg)
	return True