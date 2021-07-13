import json

class DeviceAlert:

    # data members of class
    level = 0
    date = ""
    type = ""
    description = ""
    idDevice = ""

    # class default constructor
    def __init__(self, level, date, type, description, idDevice):
        self.ipAddr = level
        self.macAddr = date
        self.netBios = type
        self.systemOS = description
        self.services = idDevice

    def updateID(self, id):
        self.id = id

    def toString(self):
        array = []
        array.append(self.level)
        array.append(self.date)
        array.append(self.type)
        array.append(self.description)
        array.append(self.idDevice)

        return json.dumps(array)
