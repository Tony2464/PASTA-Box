from requests.api import get
import scanVulnDevices
from audit.objects.Device import Device


# Get all the active devices from the network

def getActiveDevices():
    data = scanVulnDevices.requests.get(
        'http://localhost/api/devices/mapDevices')
    return data.json()


devices = getActiveDevices()
for device in devices:
    scanVulnDevices.main(Device(
        device["netBios"], device["systemOS"], device["ipAddr"], device["macAddr"], None))
