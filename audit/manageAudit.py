from audit.objects.Device import Device
import json
import datetime
import requests


# Audit configuration file
pastaAuditConfig = "/PASTA-Box/audit/config.json"


# Get the audit config from /PASTA-Box/audit/config.json

def getAuditMode():
    with open(pastaAuditConfig, encoding="utf8", errors="ignore") as configFile:
        configData = configFile.read()
        configFile.close()
    return json.loads(configData)


# Change audit mode from the HMI

def changeAuditMode(auditMode):

    try:
        mode = int(auditMode["mode"])
    except:
        return -1

    if(mode < 1 or mode > 3):
        return -1

    with open(pastaAuditConfig, "r+") as configFile:
        jsonData = json.load(configFile)
        jsonData["mode"] = mode

        configFile.seek(0)
        json.dump(jsonData, configFile, indent=4)
        configFile.truncate()
        configFile.close()

    return 0


# Add a temporary device in BDD

def addTempDevice(ipAddr: str):
    date = datetime.datetime.now()
    newDevice = {
        "ipAddr": ipAddr,
        "firstConnection": date.strftime('%Y-%m-%d %H:%M:%S'),
        "lastConnection": date.strftime('%Y-%m-%d %H:%M:%S')
    }
    jsonDeviceData = json.dumps(newDevice)
    r = requests.post('http://localhost/api/devices', json=json.loads(jsonDeviceData))

    r = requests.get('http://localhost/api/devices/', params=newDevice)
    data = r.json()
    
    device = Device(data["netBios"], data["systemOS"], data["ipAddr"], data["macAddr"], None)
    device.updateID(data["id"])
    return device
