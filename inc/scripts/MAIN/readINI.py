import configparser

def ReadINIFile(path, section, key, defaultValue = None):
    config = configparser.ConfigParser()
    config.read(path)
    try:
        return config[section][key]
    except:
        return defaultValue