import configparser

config = configparser.ConfigParser()
config.read("hw.ini")
# keys = [
#     "sunday",
#     "monday",
#     "tusday",
#     "wendsday",
#     "thursday"
# ]
def get_hw(stage, day):
	config = configparser.ConfigParser()
	config.read("hw.ini")
	value = config.get(stage, day)
	return f" ---- {day} ----\n {value}"
	config.close()

def get_hw_allweek(stage):
	config = configparser.ConfigParser()
	config.read("hw.ini")
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
	config.close()

