import os
import IpFiles
import datetime
import json
import numpy as np
import threading

# Update date in config.json

def updateDate():
    date = datetime.datetime.now()

    with open("config.json", "r+") as configFile:
        jsonData = json.load(configFile)
        jsonData["LastFetch"] = date.strftime("%d/%m/%Y")
        configFile.seek(0)
        json.dump(jsonData, configFile, indent=4)
        configFile.truncate()
        configFile.close()


# Organize the rules application

def applyEbtable(IPlist, mode):
    if(mode == True):
        res = os.system("sudo ebtables -F")
        newIPList = np.array(IPlist)
        lists = np.array_split(newIPList, 2)
        t = threading.Thread(target=addEbtableRule, args=(lists[0],))
        t.start()
        addEbtableRule(lists[1])
    else:
        addEbtableRule(IPlist)
    res = os.system(
        "sudo ebtables-nft-save > /PASTA-Box/firewall/rulesBackup.txt")


# Apply all the rules

def addEbtableRule(IPlist):
    for i in range(len(IPlist)):
        cmd = "sudo ebtables -t filter -A FORWARD -p IPv4 --ip-dst " + \
            IPlist[i].replace('\n', '') + " -j DROP"
        res = os.system(cmd)
        cmd = "sudo ebtables -t filter -A FORWARD -p IPv4 --ip-src " + \
            IPlist[i].replace('\n', '') + " -j DROP"
        res = os.system(cmd)
    

# Get all files in the repo blocklist-ipsets

def fileList(source):
    files = []
    for root, dirnames, filenames in os.walk(source):
        for filename in filenames:
            for i in range(len(IpFiles.dbAdresses)):
                if filename.find(IpFiles.dbAdresses[i]) != -1:
                    files.append(os.path.join(root, filename))
    return files


# Fetch all ip adresses

def fetchIP():
    res = os.system("cd /PASTA-Box/firewall/blocklist-ipsets && git fetch")
    listFiles = fileList("blocklist-ipsets/")
    dataIP = []

    for i in range(len(listFiles)):
        with open(listFiles[i], encoding="utf8", errors="ignore") as IPfile:
            data = IPfile.readlines()
            IPfile.close()

        for j in range(len(data)):
            if data[j].find("#") == -1:
                dataIP.append(data[j])

    dataIP = list(dict.fromkeys(dataIP))
    applyEbtable(dataIP, True)

# fetchIP()
# updateDate()