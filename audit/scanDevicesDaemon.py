import json
import requests
import threading
import subprocess
import os
import xml.etree.ElementTree as ET

from objects.Device import Device
from objects.Service import Service

# Temporary files for nmap
outputTempTcp = "/PASTA-Box/audit/temp/output_tcp.xml"
outputTempUdp = "/PASTA-Box/audit/temp/output_udp.xml"


# Get all the active devices from the network

def getActiveDevices():
    data = requests.get('http://localhost/api/devices/mapDevices')
    return data.json()


# Return protocol integer value depending of the service protocol

def protocolMode(protocol):
    if(protocol.lower() == "tcp"):
        return 1

    if(protocol.lower() == "udp"):
        return 2

    if(protocol.lower() == "icmp"):
        return 3

    return 0


# Scan devices on the network with the rights parameters (TCP or UDP)

def scanDevices(ip, mode):
    if mode == 1:  # TCP and OS/services discovery
        nmapCmd = ['sudo', 'nmap', ip, '-p-', '-sS',
                   '-sV', '-O', '-T5', '-oX', outputTempTcp]
    else:  # UDP and services discovery
        nmapCmd = ['sudo', 'nmap', ip, '-p-', '-sU',
                   '-sV', '-T5', '-oX', outputTempUdp]

    with open(os.devnull, 'wb') as devnull:
        subprocess.check_call(nmapCmd, stdout=devnull, stderr=devnull)


# Parse Nmap XML output

def parseNmap(mode, ip):
    if(mode == 1):
        xmlFile = outputTempTcp
    else:
        xmlFile = outputTempUdp

    xmlData = ET.parse(xmlFile).getroot()
    host = xmlData.find('host')

    if(host == None):
        return None

    services = []
    ports = host.find('ports')
    if(ports != None):  # Create of potential services objects in services array

        for port in ports.findall('port'):
            if(port.find('state').attrib.get('state') == "open"):

                portAttributes = port.attrib
                proto = portAttributes.get('protocol')
                serviceHost = port.find('service')

                if(serviceHost.attrib.get('product') == None or serviceHost.attrib.get('product') == ""):
                    serviceName = serviceHost.attrib.get('name')
                else:
                    serviceName = serviceHost.attrib.get('product')

                service = Service(proto, serviceName, serviceHost.attrib.get(
                    'version'), port.attrib.get('portid'))
                services.append(service)

    for address in host.findall('address'):
        if((address.attrib.get('addrtype') == "ipv4" or address.attrib.get('addrtype') == "ipv6") and address.attrib.get('addr') == ip):
            ipAddr = ip

        if(address.attrib.get('addrtype') == "mac"):
            macAddr = address.attrib.get('addr')

    hostnames = host.find('hostnames')
    hostname = hostnames.find('hostname')
    if(hostname != None):
        finalHostname = hostname.attrib.get('name')
    else:
        finalHostname = ""

    osName = ""
    if(mode == 1):  # We only determine the OS in TCP mode
        os = host.find('os')
        if(os != None):
            possibleOs = os.findall('osmatch')
            if(len(possibleOs) > 1):
                for i in range(len(possibleOs)):
                    if(possibleOs[i].attrib.get('name').find('Linux') != -1):
                        osName = "Linux"

                    if(possibleOs[i].attrib.get('name').find('Windows') != -1):
                        osName = "Windows"

            if(len(possibleOs) == 1):
                osName = possibleOs[0].attrib.get('name')

    return Device(finalHostname, osName, ipAddr, macAddr, services)


# Delete temporary XML files in temp folder

def deleteTempFile(mode):
    if(mode == 1):
        if os.path.exists(outputTempTcp):
            os.remove(outputTempTcp)
    else:
        if os.path.exists(outputTempUdp):
            os.remove(outputTempUdp)


# Update device with nmap info

def insertDevice(newDevice: Device, mode):
    addrParams = {
        'ipAddr': newDevice.ipAddr,
        'macAddr': newDevice.macAddr
    }

    data = requests.get('http://localhost/api/devices', params=addrParams)
    deviceBDD = data.json()

    if(mode == 1):

        deviceToInsert = {
            "netBios": newDevice.netBios,
            "systemOS": newDevice.systemOS
        }
        r = requests.put('http://localhost/api/devices/' +
                         str(deviceBDD["id"]), json=deviceToInsert)

    return deviceBDD["id"]


# Update device with nmap info

def insertService(newDevice: Device):
    for service in newDevice.services:

        serviceBDD = {
            "idDevice": newDevice.id,
            "numberPort": int(service.number),
            "type": int(protocolMode(service.proto)),
            "serviceName": service.name,
            "serviceVersion": service.version
        }

        r = requests.post('http://localhost/api/services', json=serviceBDD)


# Main function of the service

def main(nodes, mode):
    for i in range(len(nodes)):
        scanDevices(nodes[i]['ipAddr'], mode)
        newDevice = parseNmap(mode, nodes[i]['ipAddr'])
        if(newDevice == None):  # No insert in BDD
            continue
        else:
            deviceID = insertDevice(newDevice, mode)
            newDevice.updateID(deviceID)
            if(len(newDevice.services) != 0):
                insertService(newDevice)

        deleteTempFile(mode)


nodes = getActiveDevices()
t = threading.Thread(target=main, args=(nodes, 2,))
t.start()
main(nodes, 1)
