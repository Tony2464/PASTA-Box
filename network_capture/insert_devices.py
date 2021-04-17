from datetime import datetime
import requests
import json

# URL base of the API
def apiUrlBase(path):
    return "http://localhost/api/" + path

# Format string in GMT format
def stringToDate(string):
    return datetime.strptime(string, "%a, %d %b %Y %H:%M:%S %Z")

# Return date interval
def dayDiff(date1, date2):
    return (date1-date2)

# Insert data in API
def insertData(url, params=None):
    requests.post(url, json=params)
    return 0

# Get data from API
def getData(url, params=None):
    r = requests.get(url, params)
    data = r.json()
    return data

# Update data in API
def updateData(url, params=None):
    requests.put(url, json=params)
    return 0

# Update data in API
def updateDevice(deviceId, params):
    updateData(apiUrlBase("devices/"+deviceId), params)

# Get all the new MAC not present in device table
def getMacToInsert():
    return getData(apiUrlBase("frames/macToInsert"))

# Get last frame from MAC address
def getLastFrame(macAddr):
    params = {"limit": 1, "macSourceAndDest": macAddr}
    return getData(apiUrlBase("frames"), params)

# Get all devices
def getDevices():
    return getData(apiUrlBase("devices"))

# Insert new devices
def insertNewMac():
    macs = getMacToInsert()
    for i in range(0, len(macs)):
        params = {
            "macAddr": macs[i]["macAddr"],
            "firstConnection": str(stringToDate(macs[i]["date"]))
        }
        insertData(apiUrlBase("devices"), params)
    return 0

# Check the last IP of a device
def insertNewIp():
    devices = getDevices()
    for i in range(0, len(devices)):
        deviceMacAddr = devices[i]["macAddr"]
        frame = getLastFrame(deviceMacAddr)

        deviceIp = devices[i]["ipAddr"]
        deviceId = str(devices[i]["id"])
        frameMacAddrSource = frame[0]["macAddrSource"]
        frameIpSource = frame[0]["ipSource"]
        frameIpDest = frame[0]["ipDest"]

        # MAC source
        if (deviceMacAddr == frameMacAddrSource):
            if deviceIp != frameIpSource:
                params = {
                    "ipAddr": frameIpSource
                }
                updateDevice(deviceId, params)
        # MAC dest
        else:
            if deviceIp != frameIpDest:
                params = {
                    "ipAddr": frameIpDest
                }
                updateDevice(deviceId, params)
    return 0

# Check the last time the device has been seen
def insertNewDate():
    devices = getDevices()
    for i in range(0, len(devices)):
        deviceId = str(devices[i]["id"])
        deviceDate = None if devices[i]["lastConnection"] == None else str(
            stringToDate(str(devices[i]["lastConnection"])))
        # print(deviceDate)
        frame = getLastFrame(devices[i]["macAddr"])
        frameDate = str(stringToDate(str(frame[0]["date"])))
        if frameDate != deviceDate:
            params = {
                "lastConnection": frameDate
            }
            updateDevice(deviceId, params)
    return 0

# Check the status of a device
def insertStatus():
    with open("conf/config_insert_devices.json", "r+") as configFile:
        data = json.load(configFile)
        dayLimit = data["dayLimit"]
        devices = getDevices()
        for i in range(0, len(devices)):
            deviceId = str(devices[i]["id"])
            lastConnection = None if devices[i]["lastConnection"] == None else stringToDate(str(devices[i]["lastConnection"]))
            daysDiff = dayDiff(datetime.today(), lastConnection).days
            if (daysDiff < int(dayLimit)):
                params = {
                    "activeStatus": 1
                }
                updateDevice(deviceId, params)
            else:
                params = {
                    "activeStatus": 0
                }
                updateDevice(deviceId, params)
    return 0
