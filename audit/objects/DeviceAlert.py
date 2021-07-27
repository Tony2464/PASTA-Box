import json

class DeviceAlert:

    # data members of class
    level = 0
    date = ""
    type = ""
    description = ""

    # class default constructor
    def __init__(self, level, date, type, description):
        self.level = level
        self.date = date
        self.type = type
        self.description = description

    def toString(self):
        array = []
        array.append(self.level)
        array.append(self.date)
        array.append(self.type)
        array.append(self.description)

        return json.dumps(array)
