import yaml

def del_user(stage, uid):
	with open('config.yml', 'r') as ucfg:
		cfg = yaml.safe_load(ucfg)
		cfg['users'][stage].remove(uid)
	if cfg:
		with open('config.yml', 'w') as ucfg:
			yaml.safe_dump(cfg, ucfg)
	return True