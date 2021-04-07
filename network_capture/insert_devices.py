import requests
import json

# Get all unique and last MAC address


def getUniqueMacAddr():
    r = requests.get('http://localhost/api/frames/macAddr')
    data = r.json()
    return data

# Get last frame from MAC address


def getLastFrame(macAddr):
    req = "http://localhost/api/frames"
    params = {"limit": 1, "macSourceAndDest": macAddr}
    r = requests.get(req, params)
    data = r.json()
    return data
