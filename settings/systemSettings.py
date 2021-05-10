import json
import os
import re
import socket

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

# Settings configuration file
pastaConfigFile = "/PASTA-Box/settings/config.json"

# Temp file
pastaNetworkSettingsFile = "/PASTA-Box/settings/ipSettings.temp"

# Network bridge interface
interface = "br0"


# Check netmask

def isNetmask(string):

    octets = string.split(".")
    return len(octets) == 4 and all(o.isdigit() and 0 <= int(o) < 256 for o in octets)


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
    with open(pastaConfigFile, encoding="utf8", errors="ignore") as configFile:
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

    if(isNetmask(userConfig['netmask']) == False):
        return -5

    return 0


# Update configuration file settings/config.json

def applyConfig(userConfig):
    error = verifyConfig(userConfig)
    if(error < 0):
        return error

    with open(pastaConfigFile, "r+") as configFile:
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


# Parse network file in Raspbian

def readNetworkFile():
    with open("/etc/network/interfaces", encoding="utf8", errors="ignore") as networkFile:
        content = networkFile.readlines()
        networkFile.close()
    return content


# Read configuration files from the operating system

def parseNetworkFile():
    data = readNetworkFile()

    systemConfig = {
        "ipAddr": "",
        "netmask": "",
        "gateway": "",
        "hostname": socket.gethostname()
    }

    for i in range(len(data)):
        if(data[i].find("auto " + interface) != -1):
            i += 1
            while(i < len(data) and data[i].find("auto") == -1):
                if(data[i].find("address") != -1):
                    systemConfig['ipAddr'] = data[i].split(' ')[len(data[i].split(' ')) - 1][:-1] # Delete \n

                if(data[i].find("netmask") != -1):
                    systemConfig['netmask'] = data[i].split(' ')[len(data[i].split(' ')) - 1][:-1] # Delete \n

                if(data[i].find("gateway") != -1):
                    systemConfig['gateway'] = data[i].split(' ')[len(data[i].split(' ')) - 1][:-1] # Delete \n

                i += 1

    return systemConfig


# Change configuration files in the operating system

def updateSystemFiles(userConfig):
    localConfig = parseNetworkFile()
    if(localConfig['hostname'] != userConfig['hostname'] and localConfig['restart'] == "false"):
        os.system("sudo /PASTA-Box/settings/change_hostname.sh " + userConfig['hostname'])
        setRestart()
    
    if((localConfig['ipAddr'] != userConfig['ipAddr']) or (localConfig['netmask'] != userConfig['netmask']) or (localConfig['gateway'] != userConfig['gateway'])):
        data = readNetworkFile()
        for i in range(len(data)):
            if(data[i].find("auto " + interface) != -1): 
                i += 1
                while(i < len(data) and data[i].find("auto") == -1):
                    if(data[i].find("address") != -1):
                        data[i] = (data[i].split(' ')[0] + ' ' + userConfig['ipAddr'] + '\n')

                    if(data[i].find("netmask") != -1):
                        data[i] = (data[i].split(' ')[0] + ' ' + userConfig['netmask'] + '\n')
                    
                    if(data[i].find("gateway") != -1):
                        data[i] = (data[i].split(' ')[0] + ' ' + userConfig['gateway'] + '\n')
                    
                    i += 1
                    
        with open(pastaNetworkSettingsFile, "w") as networkTempFile:
            networkTempFile.writelines(data)
            networkTempFile.close()
        os.system("sudo /PASTA-Box/settings/change_IP.sh ")

        return data


# Set restart = true in config.json

def setRestart():
    with open(pastaConfigFile, "r+") as configFile:
        jsonData = json.load(configFile)

        jsonData["restart"] = "true"

        configFile.seek(0)
        json.dump(jsonData, configFile, indent=4)
        configFile.truncate()
        configFile.close()

# testConfig = {
#    "ipAddr": "192.168.5.2",
#    "netmask": "255.255.255.0",
#    "gateway": "192.168.5.1",
#    "hostname": "PASTA-Box"
# }
