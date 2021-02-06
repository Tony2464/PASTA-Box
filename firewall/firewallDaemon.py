import os
import json
from datetime import datetime
from os import listdir, walk
from os.path import isfile, join
from crontabs import Cron, Tab

# Apply all the rules

def applyEbtable(IPlist):
    for i in range(len(IPlist)):
        res = os.system("sudo ebtables -t filter -A FORWARD -p IPv4 --ip-dst " + IPlist[i] + " -j DROP")
    res = os.system("sudo ebtables-nft-save >> /PASTA-Box/firewall/rulesBackup.txt")


# Get all files in the repo blocklist-ipsets

def fileList(source):
    files = []
    for root, dirnames, filenames in os.walk(source):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


# Fetch all ip adresses

def fetchIP(*args, **kwargs):
    # print('args={} kwargs={} running at {}'.format(args, kwargs, datetime.now()))
    res = os.system("cd blocklist-ipsets && git fetch")
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


###### Beginning of the program ######

config = "config.json"
with open(config, encoding="utf8", errors="ignore") as configFile:
    configData = configFile.read()
    configFile.close()

jsonData = json.loads(configData)
if jsonData["Mode"] == 1: # Monthly job
    Cron().schedule(
        Tab(name="fetchIPAddr")
        .every(months=jsonData["Duration"])
        .run(fetchIP, "my_arg", my_kwarg="hello")
    ).go()
elif jsonData["Mode"] == 2: # Weekly job
    Cron().schedule(
        Tab(name="fetchIPAddr")
        .every(days=jsonData["Duration"] * 7)
        .run(fetchIP, "my_arg", my_kwarg="hello")
    ).go()
else:
    Cron().schedule(
        Tab(name="fetchIPAddr") # Daily job
        .every(days=jsonData["Duration"])
        .run(fetchIP, "my_arg", my_kwarg="hello")
    ).go()

# fetchIP()
