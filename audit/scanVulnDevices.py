import requests
import re
import datetime
import json
import os
import subprocess
import xml.etree.ElementTree as ET
from html import unescape
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
    if(service["numberPort"] == 22 or re.search('ssh', service["serviceName"], re.IGNORECASE)):
        cmd = ['sudo', 'nmap', ipAddr, "-p",
               str(service["numberPort"]), '-sV', '--script', 'ssh*.nse', '-oX', outputVulnServiceScan, '-T5']

    # Web
    if(service["numberPort"] == 80 or service["numberPort"] == 443 or re.search('http', service["serviceName"], re.IGNORECASE) or re.search('apache', service["serviceName"], re.IGNORECASE) or re.search('nginx', service["serviceName"], re.IGNORECASE)):
        cmd = ['sudo', 'nmap', ipAddr, '-p',
               str(service["numberPort"]), '-sV', '-oX', outputVulnServiceScan, '--script', 'http*.nse', '-T5']

    # DNS
    if(service["numberPort"] == 53 or re.search('dns', service["serviceName"], re.IGNORECASE)):
        cmd = ['sudo', 'nmap', ipAddr, "-p",
               str(service["numberPort"]), '-sV', '-oX', outputVulnServiceScan, '--script', 'dns*.nse', '-T5']

    # FTP
    if(service["numberPort"] == 20 or service["numberPort"] == 21 or (re.search('ftp', service["serviceName"], re.IGNORECASE) and not re.search('sftp', service["serviceName"], re.IGNORECASE))):
        cmd = ['sudo', 'nmap', ipAddr, '-p',
               str(service["numberPort"]), '-sV', '-oX', outputVulnServiceScan, '--script', 'ftp*.nse', '-T5']

    # Samba
    if(service["numberPort"] == 139 or service["numberPort"] == 445 or re.search('samba', service["serviceName"], re.IGNORECASE) or re.search('smdb', service["serviceName"], re.IGNORECASE)):
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
    jsonDeviceData = json.dumps(data)
    r = requests.put('http://localhost/api/devices/' +
                     str(id), json=json.loads(jsonDeviceData))


# Set active status on the device

def unsetScannedStatus(id):
    data = {
        "activeStatus": 1
    }
    jsonDeviceData = json.dumps(data)
    r = requests.put('http://localhost/api/devices/' +
                     str(id), json=json.loads(jsonDeviceData))


# Create and insert alert for outdated services like Telnet for example

def createOutdatedAlert(service):

    descriptions = {
        outdatedServices[0]: "Outdated protocol, Telnet is a very unsecure protocol (no encryption), please use SSH instead to prevent data interception or man in the middle attacks.",
        outdatedServices[1]: "Outdated protocol, TFTP is a very unsecure protocol (no credentials needed), please use SFTP or FTPs instead to share your files.",
        outdatedServices[2]: "Outdated protocol, RSH does not have sufficiently strong encryption,  lease use SSH instead."
    }

    date = datetime.datetime.now()
    alert = {
        "level": 4,
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
        data = {
            "level": alerts[i].level,
            # "date": date.strftime('%Y-%m-%d %H:%M:%S'),
            "date": alerts[i].date,
            "type": alerts[i].type,
            "description": alerts[i].description,
            "idDevice": id
        }
        jsonDeviceData = json.dumps(data)
        r = requests.post('http://localhost/api/alert_devices/',
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
                newAlert = DeviceAlert(1, date.strftime(
                    '%Y-%m-%d %H:%M:%S'), scripts[j].attrib.get('id'), unescape(scripts[j].attrib.get('output')))
                alerts.append(newAlert)

    if(hostscript != None):
        for script in hostscript.findall('script'):
            newAlert = DeviceAlert(1, date.strftime(
                '%Y-%m-%d %H:%M:%S'), script.attrib.get('id'), unescape(script.attrib.get('output')))
            alerts.append(newAlert)

    return alerts


# Get all the services from the device and scan them

def scanServices(device: Device, id):
    r = requests.get('http://localhost/api/services/' + str(id))
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

            insertAlert(alerts, id)
            deleteTempFile()


# Get CVE info from http://cve.mitre.org/

def getCVE(CVE: str):
    description = ""
    result = subprocess.run(['/home/nicolas/.local/bin/mitrecve', '-d', CVE], stdout=subprocess.PIPE)
    array = result.stdout.decode('utf-8').split("\n")
    for i in range(len(array)):
        if("CVE : " + CVE in array[i]):
            i += 1
            description += array[i] + '\n'

        if("NVD LINK" in array[i]):
            description += array[i] + "\n"

        if("CVE REFERENCE" in array[i]):
            description += array[i].strip() + "\n"

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
    jsonDeviceData = json.dumps(data)
    r = requests.put('http://localhost/api/devices/' +
                     str(id), json=json.loads(jsonDeviceData))


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
    isCVE = False
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
                        for elem in elems:
                            if(re.search('CVE-', elem.text)):
                                isCVE = True
                                CVE = elem.text

                        if(isCVE == True):
                            for elem in elems:
                                if(elem.attrib.get('key') == "cvss"):
                                    scoreCVSS = round(float(elem.text))
                            CVEDescription = getCVE(CVE)
                            newAlert = DeviceAlert(scoreCVSS, date.strftime(
                                '%Y-%m-%d %H:%M:%S'), "Vulnerability : " + CVE, CVEDescription)
                            alerts.append(newAlert)
                        isCVE = False

    insertSecurityScore(scoreCVSS, len(alerts), id)
    return alerts


# Scan the device with the vulners nse script from Nmap

def vulnersScan(device: Device, id):
    vulnersCmd = ['sudo', 'nmap', device.ipAddr, '-sV',
                  '--script', 'vulners', '-oX', outputVulnersScan, '-T5']
    with open(os.devnull, 'wb') as devnull:
        subprocess.check_call(vulnersCmd, stdout=devnull, stderr=devnull)

    alerts = parseNmapXMLVulners(id)
    if(alerts != None):
        insertAlert(alerts, id)

    deleteTempFile()


# Delete temporary XML files in temp folder

def deleteTempFile():

    if os.path.exists(outputVulnServiceScan):
        os.remove(outputVulnServiceScan)

    if os.path.exists(outputVulnersScan):
        os.remove(outputVulnersScan)


# Main function : scan one device per one

def main(device: Device, id):
    setScannedStatus(id)
    requests.delete('http://localhost/api/alert_devices/device' + str(id))
    scanServices(device, id)
    vulnersScan(device, id)
    unsetScannedStatus(id)
