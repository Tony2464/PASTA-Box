import json

class Device:

    # data members of class
    ipAddr = ""
    macAddr = ""
    netBios = ""
    systemOS = ""
    services = []
    id = ""

    # class default constructor
    def __init__(self, netBios, systemOS, ipAddr, macAddr, services):
        self.ipAddr = ipAddr
        self.macAddr = macAddr
        self.netBios = netBios
        self.systemOS = systemOS
        self.services = services

    def updateID(self, id):
        self.id = id

    def toString(self):
        array = []
        array.append(self.ipAddr)
        array.append(self.macAddr)
        array.append(self.netBios)
        array.append(self.systemOS)
        if (id != ""):
            array.append(self.id)

        return json.dumps(array)
