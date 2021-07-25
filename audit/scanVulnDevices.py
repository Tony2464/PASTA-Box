import requests
import re
import datetime
import json
import os
import subprocess
import xml.etree.ElementTree as ET
from html import unescape
from mitrecve import crawler
from audit.objects.Device import Device
from audit.objects.DeviceAlert import DeviceAlert

outdatedServices = [23, 69, 514]

# Temporary files for Nmap
outputVulnServiceScan = "/PASTA-Box/audit/temp/output_service.xml"
outputVulnersScan = "/PASTA-Box/audit/temp/output_vulners.xml"


# Send Nmap cmd based on the service

def returnNmapCmd(service, ipAddr):

    cmd = None

    # SSH
    if(service["numberPort"] == "22" or re.search('ssh', service["serviceName"], re.IGNORECASE) == True):
        # cmd = "sudo nmap " + ipAddr + " -p " + \
        #     str(service["numberPort"]) + \
        #     " -sV --script ssh*.nse -oX " + outputVulnServiceScan + " -T5"
        cmd = ['sudo', 'nmap', ipAddr, "-p",
               str(service["numberPort"]), '-sV', '--script', 'ssh*.nse', '-oX', outputVulnServiceScan, '-T5']

    # Web
    if(service["numberPort"] == "80" or service["numberPort"] == "443" or re.search('http', service["serviceName"], re.IGNORECASE) == True or re.search('apache', service["serviceName"], re.IGNORECASE) == True or re.search('nginx', service["serviceName"], re.IGNORECASE) == True):
        # cmd = "sudo nmap " + ipAddr + " -p " + \
        #     service["numberPort"] + \
        #     " -sV -oX " + outputVulnServiceScan + " --script http*.nse -T5"
        cmd = ['sudo', 'nmap', ipAddr, '-p', str(service["numberPort"]), '-sV', '-oX', outputVulnServiceScan, '--script', 'http*.nse', '-T5']

    # DNS
    if(service["numberPort"] == "53" or re.search('dns', service["serviceName"], re.IGNORECASE) == True):
        #cmd = "sudo nmap " + ipAddr + " -p " + \
            # str(service["numberPort"]) + \
            # " -sV -oX " + outputVulnServiceScan + " --script dns*.nse -T5"
        cmd = ['sudo', 'nmap', ipAddr, "-p", str(service["numberPort"]), '-sV', '-oX', outputVulnServiceScan, '--script', 'dns*.nse', '-T5']

    # FTP
    if(service["numberPort"] == "20" or service["numberPort"] == "21" or (re.search('ftp', service["serviceName"], re.IGNORECASE) == True and re.search('sftp', service["serviceName"], re.IGNORECASE) == False)):
        # cmd = "sudo nmap " + ipAddr + " -p " + \
        #     str(service["numberPort"]) + \
        #     " -sV -oX " + outputVulnServiceScan + " --script ftp*.nse -T5"
        cmd = ['sudo', 'nmap', ipAddr, '-p', str(service["numberPort"]), '-sV', '-oX', outputVulnServiceScan, '--script', 'ftp*.nse', '-T5']

    # Samba
    if(service["numberPort"] == "139" or service["numberPort"] == "445" or re.search('samba', service["serviceName"], re.IGNORECASE) == True or re.search('smdb', service["serviceName"], re.IGNORECASE) == False):
        # cmd = "sudo nmap " + ipAddr + " -p " + \
        #     str(service["numberPort"]) + " -sV -oX " + \
        #     outputVulnServiceScan + " --script smb*.nse -T5"
        cmd = ['sudo', 'nmap', ipAddr, '-p',
               str(service["numberPort"]), '-sV', '-oX', outputVulnServiceScan, '--script', 'smb*.nse', '-T5']

    return cmd


# Get all the services from a device

def getActiveServices(id: str):
    data = requests.get('http://localhost/api/services/' + id)
    return data.json()


# Set scanned status on the device

def setScannedStatus(id):
    data = {
        "activeStatus": 2
    }
    r = requests.put('http://localhost/api/devices/' +
                     str(id), params=data)


# Set active status on the device

def unsetScannedStatus(id):
    data = {
        "activeStatus": 1
    }
    r = requests.put('http://localhost/api/devices/' +
                     str(id), params=data)


# Create and insert alert for outdated services like Telnet for example

def createOutdatedAlert(service):

    descriptions = {
        outdatedServices[0]: "Outdated protocol, Telnet is a very unsecure protocol (no encryption), please use SSH instead to prevent data interception or man in the middle attacks.",
        outdatedServices[1]: "Outdated protocol, TFTP is a very unsecure protocol (no credentials needed), please use SFTP or FTPs instead to share your files.",
        outdatedServices[2]: "Outdated protocol, RSH does not have sufficiently strong encryption,  lease use SSH instead."
    }

    date = datetime.datetime.now()
    alert = {
        "level": 2,
        "date": date.strftime('%Y-%m-%d %H:%M:%S'),
        "type": "Outdated protocol",
        "description": descriptions.get(service["numberPort"], 1),
        "idDevice": service["idDevice"]
    }
    jsonDeviceData = json.dumps(alert)
    r = requests.post('http://localhost/api/alert_devices',
                      json=json.loads(jsonDeviceData))


# Create and insert device alert in database

def insertAlert(alerts, id):
    for i in range(len(alerts)):
        alert = {
            "level": alerts[i].level,
            # "date": date.strftime('%Y-%m-%d %H:%M:%S'),
            "date": alerts[i].date,
            "type": alerts[i].type,
            "description": unescape(alerts[i].description),
            "idDevice": id
        }
        jsonDeviceData = json.dumps(alert)
        r = requests.post('http://localhost/api/alert_devices',
                          json=json.loads(jsonDeviceData))


# Parse XML Nmap output from the service scan

def parseNmapXMLService():
    xmlFile = outputVulnServiceScan
    xmlData = ET.parse(xmlFile).getroot()
    host = xmlData.find('host')

    if(host == None):
        return None

    ports = host.find('ports')
    hostscript = host.find('hostscript')

    if(ports == None and hostscript == None):
        return None

    date = datetime.datetime.now()
    alerts = []
    if(ports != None):
        for port in ports.findall('port'):
            scripts = port.findall('script')
            if(scripts == None):
                continue

            for j in range(len(scripts)):
                newAlert = DeviceAlert(2, date.strftime(
                    '%Y-%m-%d %H:%M:%S'), scripts[j].attrib.get('id'), scripts[j].attrib.get('output'))
                alerts.append(newAlert)

    if(hostscript != None):
        for script in scripts.findall('port'):
            newAlert = DeviceAlert(2, date.strftime(
                '%Y-%m-%d %H:%M:%S'), script.attrib.get('id'), script.attrib.get('output'))
            alerts.append(newAlert)

    return alerts


# Get all the services from the device and scan them

def scanServices(device: Device):
    r = requests.get('http://localhost/api/services/' + str(device.id))
    services = r.json()

    for i in range(len(services)):
        if services[i]["numberPort"] in outdatedServices:
            createOutdatedAlert(services[i])
        else:
            cmd = returnNmapCmd(services[i], device.ipAddr)
            if(cmd == None):  # No Nmap cmd based on this service
                continue

            with open(os.devnull, 'wb') as devnull:
                subprocess.check_call(cmd, stdout=devnull, stderr=devnull)

            alerts = parseNmapXMLService()
            if(alerts == None):  # No vuln detected on this service
                continue

            insertAlert(alerts, device.id)
            deleteTempFile()


# Get CVE info from http://cve.mitre.org/

def getCVE(CVE: str):
    data = crawler.get_cve_detail(CVE)
    description = data[0][1] + "\n"
    for link in data[0][2]:
        description += link
        description += "\n"

    return description


# Calculate and insert in database the security score

def insertSecurityScore(scoreCVSS, nbAlerts, id):
    if(nbAlerts == 0):
        value = 0
    else:
        value = scoreCVSS / nbAlerts
        value = round(value, 1)
    
    newScore = 10 - value
    data = {
        "securityScore": newScore
    }
    r = requests.put('http://localhost/api/devices/' + str(id), params=data)


# Parse XML Nmap output from the vulners NSE script

def parseNmapXMLVulners(id):
    xmlFile = outputVulnersScan
    xmlData = ET.parse(xmlFile).getroot()
    host = xmlData.find('host')

    if(host == None):
        return None

    ports = host.find('ports')
    alerts = []
    scoreCVSS = 0
    date = datetime.datetime.now()
    if(ports != None):
        for port in ports.findall('port'):
            scripts = port.findall('script')
            if(scripts == None):
                continue
            for script in scripts:
                if(script.attrib.get("id") == "vulners"):
                    for table in script.find("table").findall('table'):
                        elems = table.findall("elem")
                        if(elems[1] == "cve"):
                            CVE = elems[0].text
                            scoreCVSS += float(elems[2].text)
                            CVEDescription = getCVE(CVE)
                            newAlert = DeviceAlert(3, date.strftime(
                                '%Y-%m-%d %H:%M:%S'), "Vulnerability : " + CVE, CVEDescription)
                            alerts.append(newAlert)

    insertSecurityScore(scoreCVSS, len(alerts), id)
    return alerts


# Scan the device with the vulners nse script from Nmap

def vulnersScan(device: Device):
    vulnersCmd = ['sudo', 'nmap', device.ipAddr, '-sV', '--script', 'vulners', '-oX', outputVulnersScan, '-T5']
    with open(os.devnull, 'wb') as devnull:
        subprocess.check_call(vulnersCmd, stdout=devnull, stderr=devnull)

    alerts = parseNmapXMLVulners(device.id)
    if(alerts != None):
        insertAlert(alerts, device.id)
    
    deleteTempFile()


# Delete temporary XML files in temp folder

def deleteTempFile():

    if os.path.exists(outputVulnServiceScan):
        os.remove(outputVulnServiceScan)

    if os.path.exists(outputVulnersScan):
        os.remove(outputVulnersScan)


# Main function : scan one device per one

def main(device: Device, id):
    setScannedStatus(device)
    requests.delete('http://localhost/api/alert_devices/' + str(device.id))
    scanServices(device)
    vulnersScan(device)
    unsetScannedStatus(device)