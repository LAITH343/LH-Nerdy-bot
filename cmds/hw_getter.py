import configparser

config = configparser.ConfigParser()
config.read("storage/hw.ini")
# keys = [
#     "sunday",
#     "monday",
#     "tusday",
#     "wendsday",
#     "thursday"
# ]
def get_hw(stage, day):
	config = configparser.ConfigParser()
	config.read("storage/hw.ini")
	value = config.get(stage, day)
	return f" ---- {day} ----\n {value}"


def get_hw_allweek(stage):
	config = configparser.ConfigParser()
	config.read("storage/hw.ini")
	week = ""
	keys = [
	    "الاحد",
	    "الاثنين",
	    "الثلاثاء",
	    "الاربعاء",
	    "الخميس"
	]
	for key in keys:
		value = config.get(stage, key)
		week += f"---- {key} ----\n {value}\n"
	return week

