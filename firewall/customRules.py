import re
import os
from ipaddress import ip_address, IPv4Address


# Check IP version

def checkIP(IP):
    try:
        return 1 if type(ip_address(IP)) is IPv4Address else 2
    except ValueError:
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
