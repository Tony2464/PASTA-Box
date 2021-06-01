import nmap
import requests
import collections

scanner = nmap.PortScanner()
ScanType = collections.namedtuple("ScanType", "proto args")
scan_types = {

    1: ScanType(proto="tcp", args="-v -sS -sV -sC -O"),
    2: ScanType(proto="udp", args="-v -sU -sV")
}


# Get all the active devices from the network

def getActiveDevices():
    data = requests.get('http://localhost/api/devices/mapDevices')
    return data.json
