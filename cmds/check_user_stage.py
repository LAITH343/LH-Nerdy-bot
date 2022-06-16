import yaml

def check_stage(uid):
	with open('config.yml', 'r') as ucfg:
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