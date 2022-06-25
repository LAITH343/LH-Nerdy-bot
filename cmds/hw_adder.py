import configparser


def add_hw(stage, day, m):
    # Writing Data
    config = configparser.ConfigParser()
    config.read("storage/hw.ini")
    config.set(str(stage), day, m)
    with open("storage/hw.ini", "w") as config_file:
        config.write(config_file)
    return True
