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

def check_user_stage_name(uid):
	with open('storage/users_info.yml', 'r') as ucfg:
		cfg = yaml.safe_load(ucfg)
		stage1 = cfg['users']['stage1']
		stage2 = cfg['users']['stage2']
		stage3 = cfg['users']['stage3']
		stage4 = cfg['users']['stage4']
	if uid in stage1:
		return "اولى"
	elif uid in stage2:
		return "ثانية"
	elif uid in stage3:
		return "ثالثة"
	elif uid in stage4:
		return "رابعة"
	else:
		return "انت لا تنتمي ﻷي مرحلة"
	cfg.close()

def get_manager_stage(uid):
	with open('storage/users_info.yml', 'r') as ucfg:
		cfg = yaml.safe_load(ucfg)
		stage1 = cfg['managers']['stage1']
		stage2 = cfg['managers']['stage2']
		stage3 = cfg['managers']['stage3']
		stage4 = cfg['managers']['stage4']
	if uid in stage1:
		return 1
	elif uid in stage2:
		return 2
	elif uid in stage3:
		return 3
	elif uid in stage4:
		return 4
	else:
		return False



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

def add_manager(stage, uid):
	with open('storage/users_info.yml', 'r') as ucfg:
		cfg = yaml.safe_load(ucfg)
		cfg['managers'][stage].append(uid)
	if cfg:
		with open('storage/users_info.yml', 'w') as ucfg:
			yaml.safe_dump(cfg, ucfg)
	return True

def del_manager(stage, uid):
	with open('storage/users_info.yml', 'r') as ucfg:
		cfg = yaml.safe_load(ucfg)
		cfg['managers'][stage].remove(uid)
	if cfg:
		with open('storage/users_info.yml', 'w') as ucfg:
			yaml.safe_dump(cfg, ucfg)
	return True

def get_users_uid(uid):
	with open('storage/users_info.yml', 'r') as ucfg:
		cfg = yaml.safe_load(ucfg)
		stage1 = cfg['users']['stage1']
		stage2 = cfg['users']['stage2']
		stage3 = cfg['users']['stage3']
		stage4 = cfg['users']['stage4']
	ul = []
	if get_manager_stage(uid) == 1:
		stage = stage1
	elif get_manager_stage(uid) == 2:
		stage = stage2
	elif get_manager_stage(uid) == 3:
		stage = stage3
	elif get_manager_stage(uid) == 4:
		stage = stage4
	
	for i in stage:
		ul.append(i)
	ul.remove(uid)
	return ul

def get_users_uid_all(uid):
	with open('storage/users_info.yml', 'r') as ucfg:
		cfg = yaml.safe_load(ucfg)
		stage1 = cfg['users']['stage1']
		stage2 = cfg['users']['stage2']
		stage3 = cfg['users']['stage3']
		stage4 = cfg['users']['stage4']
	ul = []
	
	for i in stage1:
		ul.append(i)
	for i in stage2:
		ul.append(i)
	for i in stage3:
		ul.append(i)
	for i in stage4:
		ul.append(i)
	ul.remove(uid)
	return ul