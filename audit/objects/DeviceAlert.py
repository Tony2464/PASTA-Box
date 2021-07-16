import json

class DeviceAlert:

    # data members of class
    level = 0
    date = ""
    type = ""
    description = ""

    # class default constructor
    def __init__(self, level, date, type, description):
        self.ipAddr = level
        self.macAddr = date
        self.netBios = type
        self.systemOS = description

    def toString(self):
        array = []
        array.append(self.level)
        array.append(self.date)
        array.append(self.type)
        array.append(self.description)

        return json.dumps(array)
