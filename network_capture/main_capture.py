#!/usr/bin/env python3

import os
import sys

# local imports
from conf import config as config

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

        # Executing the capture
        os.system("sudo tshark " +
                  buffer +
                  " -i " + config.interface +
                  " -T fields -E separator='" + separator + "' " +
                  formattedFields +
                  " | " + "python3 " + insertProgram)
    except KeyboardInterrupt:
        sys.stdout.flush()
        pass

if __name__ == "__main__":
    main()
