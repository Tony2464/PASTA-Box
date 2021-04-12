import os
import json


# Get the PASTA-Box configuration from settings/config.json

def getConfig():
    config = "/PASTA-Box/settings/config.json"
    with open(config, encoding="utf8", errors="ignore") as configFile:
        configData = configFile.read()
        configFile.close()
    return json.loads(configData)
