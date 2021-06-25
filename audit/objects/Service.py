import json

class Service:

    #data members of class
    proto = ""
    name = ""
    version = ""
    number = ""

    #class default constructor
    def __init__(self, proto, name, version, number):
        self.proto = proto
        self.name = name
        self.version = version
        self.number = number

    def toString(self):
        array = []
        array.append(self.proto)
        array.append(self.name)
        array.append(self.version)
        array.append(self.number)

        return json.dumps(array)
