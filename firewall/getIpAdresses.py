import os
import IpFiles

# Apply all the rules

def applyEbtable(IPlist, mode):
    if(mode == True):
        res = os.system("sudo ebtables -F")

    for i in range(len(IPlist)):
        cmd = "sudo ebtables -t filter -A FORWARD -p IPv4 --ip-dst " + \
            IPlist[i].replace('\n', '') + " -j DROP"
        res = os.system(cmd)
        cmd = "sudo ebtables -t filter -A FORWARD -p IPv4 --ip-src " + \
            IPlist[i].replace('\n', '') + " -j DROP"
        res = os.system(cmd)
    res = os.system(
        "sudo ebtables-nft-save > /PASTA-Box/firewall/rulesBackup.txt")


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
    applyEbtable(dataIP, True)

    # backup = open("test.txt", "a")
    # backup.writelines(dataIP)
    # backup.close()

fetchIP()