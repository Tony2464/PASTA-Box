import os
import IpFiles
import datetime
import json
import numpy as np
import threading
import re

# Regex IPv4
ipv4 = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(  
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(  
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(  
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''

# Regex IPv6
ipv6 = '''(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}| 
        ([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:) 
        {1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1 
        ,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4} 
        :){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{ 
        1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA 
        -F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a 
        -fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0 
        -9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0, 
        4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1} 
        :){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9 
        ])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0 
        -9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4] 
        |1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4] 
        |1{0,1}[0-9]){0,1}[0-9]))'''


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


# Check IP version

def checkIP(string):
    if re.search(ipv4, string):
        return 1
    elif re.search(ipv6, string):
        return 2
    else:
        return 3


# Check if the rule parameters are correct

def verifyRule(Rule):
    if(Rule["protocol"] < 0 or Rule["protocol"] > 3):
        return -1

    if(Rule["protocol"] == 3):
        if(Rule["ipDst"] == None and Rule["ipSource"] == None):
            return -2

    if(Rule["portSrc"] == None or Rule["portDst"] == None):
        if(Rule["ipDst"] == None and Rule["ipSource"] == None):
            return -3

    if(Rule["ipDst"] != None):
        Rule["ipDstVersion"] = checkIP(Rule["ipDst"])
        if(Rule["ipDstVersion"] == 3):
            return -4

    if(Rule["ipSrc"] != None):
        Rule["ipSrcVersion"] = checkIP(Rule["ipSrc"])
        if(Rule["ipSrcVersion"] == -3):
            return 5
        if(Rule["ipVersion"] != Rule["ipDstVersion"]):
            return -6

    return 0


# Apply customized rules from the HMI

def buildCustomRules(Rule):
    error = verifyRule(Rule)
    if(error < 0):
        return error

    cmd = "sudo ebtables -t filter -A FORWARD "
    if(Rule["ipSrcVersion"] == 1 or Rule["ipDstVersion"] == 1):
        cmd += "-p ipv4 "
        version = "ipv4"
        if(Rule["ipSrc"] != None):
            cmd += "--ip-src " + Rule["ipSrc"] + " "
        if(Rule["ipDst"] != None):
            cmd += "--ip-dst " + Rule["ipDst"] + " "

    elif(Rule["ipSrcVersion"] == 2 or Rule["ipDstVersion"] == 2):
        cmd += "-p ipv6 "
        version = "ipv6"
        if(Rule["ipSrc"] != None):
            cmd += "--ip6-source " + Rule["ipSrc"] + " "
        if(Rule["ipDst"] != None):
            cmd += "--ip6-destination " + Rule["ipDst"] + " "

    if(Rule["protocol"] != None):

        if(version == "ipv4"):
            cmd += "--ip-protocol "
            if(Rule["protocol"] == 1):
                cmd += "tcp "
            elif(Rule["protocol"] == 2):
                cmd += "udp "
            else:
                cmd += "icmp "

            if(Rule["protocol"] != 3):
                if(Rule["portSrc"] != None):
                    cmd += "--ip-source-port " + Rule["portSrc"]
                else:
                    cmd += "--ip-destination-port " + Rule["portDst"]

        else:
            cmd += "--ip6-protocol "
            if(Rule["protocol"] == 1):
                cmd += "tcp "
            elif(Rule["protocol"] == 2):
                cmd += "udp "
            else:
                cmd += "icmp "

            if(Rule["protocol"] != 3):
                if(Rule["portSrc"] != None):
                    cmd += "--ip6-source-port " + Rule["portSrc"]
                else:
                    cmd += "--ip6-destination-port " + Rule["portDst"]
    cmd += "-j DROP"
    res = os.system(cmd)


# Organize the rules application in background

def applyEbtableBack(IPlist):
    res = os.system("sudo ebtables -F")
    newIPList = np.array(IPlist)
    lists = np.array_split(newIPList, 2)
    t = threading.Thread(target=addEbtableRule, args=(lists[0],))
    t.start()
    addEbtableRule(lists[1])
    res = os.system(
        "sudo ebtables-nft-save > /PASTA-Box/firewall/rulesBackup.txt")


# Apply the rules from the repo blocklist-ipsets

def addEbtableRule(IPlist):
    for i in range(len(IPlist)):
        ipAddr = IPlist[i].replace('\n', '')
        cmd = "sudo ebtables -t filter -A FORWARD -p IPv4 --ip-dst " + ipAddr + " -j DROP"
        res = os.system(cmd)
        cmd = "sudo ebtables -t filter -A FORWARD -p IPv4 --ip-src " + ipAddr + " -j DROP"
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
    applyEbtableBack(dataIP)

# fetchIP()
# updateDate()
