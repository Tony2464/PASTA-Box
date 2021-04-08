from datetime import datetime
from flask.helpers import get_load_dotenv
import requests

# Api url base


def apiUrlBase(path):
    return "http://localhost/api/" + path

# convert string to date format


def stringToDate(string):
    return str(datetime.strptime(string, "%a, %d %b %Y %H:%M:%S %Z"))

# Insert data with API


def insertData(url, params=None):
    requests.post(url, json=params)
    return 0


def getData(url, params=None):
    r = requests.get(url, params)
    data = r.json()
    return data


# Get all unique and last MAC address

# def getUniqueMacAddr():
#     r = requests.get('http://localhost/api/frames/macAddr')
#     data = r.json()
#     return data

# Get MAC to insert


def getMacToInsert():
    return getData(apiUrlBase("frames/macToInsert"))

# Get last frame from MAC address


def getLastFrame(macAddr):
    params = {"limit": 1, "macSourceAndDest": macAddr}
    return getData(apiUrlBase("frames"), params)

# Get all devices


def getDevices():
    return getData(apiUrlBase("devices"))


# Insert new mac


def insertNewMac():
    macs = getMacToInsert()
    for i in range(0, len(macs)):
        params = {
            "macAddr": macs[i]["macAddr"],
            "firstConnection": stringToDate(macs[i]["date"])
        }
        insertData(apiUrlBase("devices"), params)
    return 0

def insertNewIp():
    devices = getDevices()
    return 0
