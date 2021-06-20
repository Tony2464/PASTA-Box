import json
from objects.Service import Service

class Device:

    # data members of class
    ipAddr = ""
    macAddr = ""
    netBios = ""
    systemOS = ""
    services = []

    # class default constructor
    def __init__(self, netBios, systemOS, ipAddr, macAddr, services):
        self.ipAddr = ipAddr
        self.macAddr = macAddr
        self.netBios = netBios
        self.systemOS = systemOS
        self.services = services

    def toString(self):
        array = []
        array.append(self.ipAddr)
        array.append(self.macAddr)
        array.append(self.netBios)
        array.append(self.systemOS)

        return json.dumps(array)
