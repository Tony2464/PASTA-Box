import re
import os


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
    ipSrcVersion = 0
    ipDstVersion = 0
    if(int(Rule["protocol"]) < 0 or int(Rule["protocol"]) > 3):
        return -1

    if(int(Rule["protocol"]) == 3):
        if(Rule["ipDst"] == "" and Rule["ipSrc"] == ""):
            return -2

    if(Rule["portSrc"] == "" and Rule["portDst"] == ""):
        if(Rule["ipDst"] == "" and Rule["ipSrc"] == ""):
            return -3

    if(Rule["ipDst"] != ""):
        ipDstVersion = checkIP(Rule["ipDst"])
        if(ipDstVersion == 3):
            return -4

    if(Rule["ipSrc"] != ""):
        ipSrcVersion = checkIP(Rule["ipSrc"])
        if(ipSrcVersion == 3):
            return -5
        if(Rule["ipVersion"] != ipDstVersion and ipDstVersion != 0):
            return -6

    if(ipSrcVersion != 0 and ipDstVersion != 0 and ipDstVersion != ipSrcVersion):
        return -6

    if(Rule["portSrc"] != "" and (int(Rule["portSrc"]) < 1 or int(Rule["portSrc"]) > 65535)):
        return -7

    if(Rule["portDst"] != "" and (int(Rule["portDst"]) < 1 or int(Rule["portDst"]) > 65535)):
        return -8

    return 0


# Apply customized rules from the HMI

def buildCustomRules(Rule):
    error = verifyRule(Rule)
    if(error < 0):
        return error

    exception = False
    cmd = "sudo ebtables -t filter -A FORWARD "
    if(Rule["ipVersion"] == 1):
        cmd += "-p ipv4 "
        version = "ipv4"
        if(Rule["ipSrc"] != None):
            cmd += "--ip-src " + Rule["ipSrc"] + " "
        if(Rule["ipDst"] != None):
            cmd += "--ip-dst " + Rule["ipDst"] + " "

    elif(Rule["ipVersion"] == 2):
        cmd += "-p ipv6 "
        version = "ipv6"
        if(Rule["ipSrc"] != None):
            cmd += "--ip6-source " + Rule["ipSrc"] + " "
        if(Rule["ipDst"] != None):
            cmd += "--ip6-destination " + Rule["ipDst"] + " "

    else:
        exception = True

    if(Rule["protocol"] != None):

        if(Rule["ipVersion"] == 1):
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

    if(exception == True):
        res = os.system(cmd.replace('--ip6-protocol', '--ip-protocol'))

    return 0
