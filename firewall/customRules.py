import re
import os
import requests
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
    if int(Rule["protocol"]) < 0 or int(Rule["protocol"]) > 3:
        return -1

    if int(Rule["protocol"]) == 3:
        if Rule["ipDst"] == "" and Rule["ipSrc"] == "":
            return -2

    if Rule["portSrc"] == "" and Rule["portDst"] == "":
        if Rule["ipDst"] == "" and Rule["ipSrc"] == "":
            return -3

    if Rule["ipDst"] != "":
        ipDstVersion = checkIP(Rule["ipDst"])
        if ipDstVersion == 3:
            return -4

    if Rule["ipSrc"] != "":
        ipSrcVersion = checkIP(Rule["ipSrc"])
        if ipSrcVersion == 3:
            return -5
        if Rule["ipVersion"] != ipDstVersion and ipDstVersion != 0:
            return -6

    if ipSrcVersion != 0 and ipDstVersion != 0 and ipDstVersion != ipSrcVersion:
        return -6

    if (
        Rule["portSrc"] != ""
        and Rule["portSrc"] != None
        and (
            Rule["portSrc"] == ""
            or int(Rule["portSrc"]) < 1
            or int(Rule["portSrc"]) > 65535
        )
    ):
        return -7

    if (
        Rule["portDst"] != ""
        and Rule["portDst"] != None
        and (
            Rule["portDst"] == ""
            or int(Rule["portDst"]) < 1
            or int(Rule["portDst"]) > 65535
        )
    ):
        return -8

    return 0


# Build customized rules from json

def buildCustomRules(Rule, mode):

    if mode == True:  # Verify the rule only if it just has been added
        error = verifyRule(Rule)
        if error < 0:
            return error

    exceptionIP = False
    exceptionProto = False

    cmd = beginEbtablesCmd(mode)

    if int(Rule["ipVersion"]) == 1:  # IPv4 ?
        cmd += "-p ipv4 "

        if (Rule["portSrc"] != None and Rule["portSrc"] != "") or (
            Rule["portDst"] != None and Rule["portDst"] != ""
        ):
            cmd += "--ip-protocol "
            if int(Rule["protocol"]) == 1:
                cmd += "tcp "
            elif int(Rule["protocol"]) == 2:
                cmd += "udp "
            elif int(Rule["protocol"]) == 2:
                cmd += "icmp "
            else:
                cmd += "all "
                exceptionProto = True

        if Rule["ipSrc"] != None and Rule["ipSrc"] != "":
            cmd += "--ip-src " + Rule["ipSrc"] + " "
        if Rule["ipDst"] != None and Rule["ipDst"] != "":
            cmd += "--ip-dst " + Rule["ipDst"] + " "

    elif int(Rule["ipVersion"]) == 2:  # IPv6 ?
        cmd += "-p ipv6 "

        if (Rule["portSrc"] != None and Rule["portSrc"] != "") or (
            Rule["portDst"] != None and Rule["portDst"] != ""
        ):
            cmd += "--ip6-protocol "
            if int(Rule["protocol"]) == 1:
                cmd += "tcp "
            elif int(Rule["protocol"]) == 2:
                cmd += "udp "
            elif int(Rule["protocol"]) == 2:
                cmd += "icmp "
            else:
                cmd += "all "
                exceptionProto = True

        if Rule["ipSrc"] != None and Rule["ipSrc"] != "":
            cmd += "--ip6-source " + Rule["ipSrc"] + " "
        if Rule["ipDst"] != None and Rule["ipDst"] != "":
            cmd += "--ip6-destination " + Rule["ipDst"] + " "

    else:  # No IP address specified
        cmd += "-p ipv4 --ip-protocol "
        exceptionIP = True

    if int(Rule["ipVersion"]) == 1:

        if int(Rule["protocol"]) != 3:
            if Rule["portSrc"] != None and Rule["portSrc"] != "":
                cmd += "--ip-source-port " + str(Rule["portSrc"]) + " "
            if Rule["portDst"] != None and Rule["portDst"] != "":
                cmd += "--ip-destination-port " + str(Rule["portDst"]) + " "

    elif int(Rule["ipVersion"]) == 2:

        if int(Rule["protocol"]) != 3:
            if Rule["portSrc"] != None and Rule["portSrc"] != "":
                cmd += "--ip6-source-port " + str(Rule["portSrc"]) + " "
            if Rule["portDst"] != None and Rule["portDst"] != "":
                cmd += "--ip6-destination-port " + str(Rule["portDst"]) + " "

    cmd += "-j DROP"

    # If there isn't ip src/dst address but one port at least (dst or src port)

    if exceptionIP == True and exceptionProto == False:
        res = os.system(cmd)
        res = os.system(
            cmd.replace("-p ipv4 --ip-protocol ", "-p ipv6 --ip6-protocol ")
        )

    # If all protocols were selected and one port at least (dst or src port)

    elif exceptionProto == True:
        cmds = cmd.split("all")
        for i in range(len(ebtablesPortProtocols)):
            res = os.system(cmds[0] + str(ebtablesPortProtocols[i]) + cmds[1])

        # Apply for IPv6 if any specific type of ip ardress was selected

        if exceptionIP == True:
            cmdIpv6 = cmd.replace("-p ipv4 --ip-protocol ", "-p ipv6 --ip6-protocol ")
            cmdsIpv6 = cmdIpv6.split("all")
            for i in range(len(ebtablesPortProtocols)):
                res = os.system(
                    cmdsIpv6[0] + str(ebtablesPortProtocols[i]) + cmdsIpv6[1]
                )

    # No exception

    else:
        res = os.system(cmd)

    return 0


# Get all the rules from the database

def getAllCustomRules():
    
    r = requests.get("http://localhost/api/rules")
    data = r.json()
    for i in range(len(data)):
        buildCustomRules(data[i])


# Send the correct beginning of the command

def beginEbtablesCmd(mode):

    if mode == True:
        cmd = "/usr/bin/sudo /usr/sbin/ebtables -t filter -A FORWARD "  # Add rule in RAM
    else:
        cmd = "/usr/bin/sudo /usr/sbin/ebtables -t filter -D FORWARD "  # Delete rule in RAM
    return cmd
