#!/usr/bin/env python3

import sys
sys.path.append("..")

# Local imports
from conf import config
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

# Get data from stdin
for line in sys.stdin:
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
    applicationLayer = protocol[4] if len(protocol) == 5 else None

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
         protocol[2],  # network layer
         frame[12],  # DNS query
         frame[13],  # Info
         )
    )
