import os
import json
import re

# Regex IPv4
ipv4 = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(  
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(  
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(  
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''

# Regex IPv6
ipv6 = '''(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}| 
        ([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:) 
        {1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1 
        ,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4} 
        :){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{ 
        1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA 
        -F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a 
        -fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0 
        -9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0, 
        4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1} 
        :){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9 
        ])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0 
        -9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4] 
        |1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4] 
        |1{0,1}[0-9]){0,1}[0-9]))'''

# Regex hostname
hostname = '''^([a-zA-Z0-9](?:(?:[a-zA-Z0-9-]*|(?<!-)\.(?![-.]))*[a-zA-Z0-9]+)?)$'''


# Check IP version

def checkIP(string):
    if re.search(ipv4, string):
        return 1
    elif re.search(ipv6, string):
        return 2
    else:
        return 3


# Get the PASTA-Box configuration from settings/config.json

def getConfig():
    config = "/PASTA-Box/settings/config.json"
    with open(config, encoding="utf8", errors="ignore") as configFile:
        configData = configFile.read()
        configFile.close()
    return json.loads(configData)


# Check if the config parameters are correct

def verifyConfig(userConfig):
    if(checkIP(userConfig['ipAddr']) == 3):
        return -1

    if(checkIP(userConfig['gateway']) == 3):
        return -2

    if(re.search(hostname, userConfig['hostname']) == False):
        return -3

    if(len(userConfig['hostname']) > 255 or len(userConfig['hostname']) == 0):
        return -4

    if(checkIP(userConfig['netmask']) == 3):
        return -5

    return 0


# Update configuration file settings/config.json

def applyConfig(userConfig):
    error = verifyConfig(userConfig)
    if(error < 0):
        return error

    with open("config.json", "r+") as configFile:
        jsonData = json.load(configFile)

        jsonData["ipAddr"] = userConfig['ipAddr']
        jsonData["hostname"] = userConfig['hostname']
        jsonData["gateway"] = userConfig['gateway']
        jsonData["netmask"] = userConfig['netmask']

        configFile.seek(0)
        json.dump(jsonData, configFile, indent=4)
        configFile.truncate()
        configFile.close()

    return 0
