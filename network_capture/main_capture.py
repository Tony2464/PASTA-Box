#!/usr/bin/env python3

import sys
from subprocess import Popen, PIPE

# local imports
from conf import config as config
from database import db_manager

dbManager = db_manager.DbManager(
    config.dbConfig["user"],
    config.dbConfig["password"],
    config.dbConfig["host"],
    config.dbConfig["port"],
    config.dbConfig["database"]
)

# Insert information
count = 0
srcport = ""
dstport = ""
protocol = ""
applicationLayer = ""
srcIp = ""
dstIp = ""

insertProgram = "insert_capture.py"  # With extension
separator = "|"
fields = [
    # Ports (TCP and UDP)
    "tcp.srcport",
    "tcp.dstport",
    "udp.srcport",
    "udp.dstport",

    # IP@ (IPv4 and IPv6)
    "ip.src",
    "ip.dst",
    "ipv6.src",
    "ipv6.dst",

    # MAC@
    "eth.src",
    "eth.dst",

    # Transport layer (number)
    "frame.protocols",

    # Application and network layers
    "ip.proto",

    # Domain name
    "dns.qry.name",

    # Some info
    "_ws.col.Info"

]  # Chronological order


def main():
    try:
        # Format Buffer
        buffer = "-B " + \
            config.bufferSize if int(config.bufferSize) != 0 else ""

        # Format all the fields
        formattedFields = ""
        for i in range(0, len(fields)):
            formattedFields += "-e " + fields[i] + " "

        cmd = "sudo tshark " + buffer + " -i " + config.interface + " -T fields -E separator='" + separator + "' " + formattedFields
        with Popen(cmd, shell=True, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
            for line in p.stdout:
                frame = line.split("|")

                # Determine tcp port or udp port
                if frame[0]:  # Tcp port
                    srcport = frame[0]
                    dstport = frame[1]
                else:  # Udp port
                    srcport = frame[2]
                    dstport = frame[3]

                # Determine ipv4 or ipv6
                if frame[4]:  # ipv4
                    srcIp = frame[4]
                    dstIp = frame[5]
                else:
                    srcIp = frame[6]
                    dstIp = frame[7]

                # Determine application layer
                protocol = frame[10].split(":")
                # For LLC problem
                if len(protocol) > 2:
                    applicationLayer = protocol[4] if len(protocol) == 5 else None
                    networkLayer = protocol[2]
                else:
                    applicationLayer = None
                    networkLayer = None
                # Insertion
                dbManager.queryInsert(
                    "INSERT INTO `Frame` (`portSource`, `portDest`, `ipSource`, `ipDest`, `macAddrSource`, `macAddrDest`, `protocolLayerApplication`, `protocolLayerTransport`, `protocolLayerNetwork`, `date`, `domain`, `info`) VALUES(%s, %s, %s, %s,%s, %s, %s, %s, %s, CURRENT_TIME(), %s, %s)",
                    (srcport,
                    dstport,
                    srcIp,
                    dstIp,
                    frame[8],  # mac src
                    frame[9],  # mac dst
                    applicationLayer,  # application layer
                    frame[11],  # transport layer
                    networkLayer,  # network layer
                    frame[12],  # DNS query
                    frame[13],  # Info
                    )
                )

    except KeyboardInterrupt:
        sys.stdout.flush()
        pass

if __name__ == "__main__":
    main()
