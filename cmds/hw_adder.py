import configparser


def add_hw(stage, day, m):
    # Writing Data
    config = configparser.ConfigParser()
    config.read("storage/hw.ini")
    config.set(stage, day, m)
    with open("storage/hw.ini", "w") as config_file:
        config.write(config_file)
    return True

# Reading Data
# config.read(filename)
# keys = [
#     "sunday",
#     "monday",
#     "tusday",
#     "wendsday",
#     "thursday"
# ]
# for key in keys:
#     try:
#         value = config.get("first_stage", key)
#         print(f"{key}:", value)
#     except configparser.NoOptionError:
#         print(f"No option '{key}' in section 'first_stage'")