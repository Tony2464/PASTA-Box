#!/usr/bin/python

import datetime
import conf.config as config
import os
import sys
sys.path.append("./conf")

insertProgram = "insert_capture.py"  # With extension
separator = ","
fields = [
    # Ports  DONE
    # "tcp.port",
    # "udp.port",
    "tcp.srcport",
    "tcp.dstport",
    "udp.srcport",
    "udp.dstport",

    # IP@ DONE
    # "ip.addr",
    "ip.src",
    "ip.dst",

    # MAC @ DONE
    # "eth.addr",
    "eth.src",
    "eth.dst",

    # Applciation Layer
    # NOTE DONE

    # Transport Layer DONE UDP or TCP
    "frame.protocols",
    "ip.proto",
    
    # Network layer
    # "_ws.col.Protocol",
    
    # "timestamp"
    # "frame.time",


    # Domaine name DONE
    "dns.qry.name"

]  # Chronological order


def main():
    # Funny can't stop the programm
    # try:
    #     while True:
    #         os.system("sudo tshark -i eth0 -T fields -E separator=, -e ip.src -e ip.dst -e _ws.col.Protocol -e _ws.col.Info")
    #         # os.system("echo Hi")
    # except KeyboardInterrupt:
    #     sys.stdout.flush()
    #     pass
    try:
        # Format Buffer
        buffer = "-B " + \
            config.bufferSize if int(config.bufferSize) != 0 else ""

        # Format all the fields
        formattedFields = ""
        for i in range(0, len(fields)):
            formattedFields += "-e " + fields[i] + " "

        # Executing the capture
        os.system("sudo tshark " + buffer + " -i " + config.interface +
                  " -T fields -E separator='" + separator + "' " +
                  formattedFields
                 + " | " + "python3 " + insertProgram)
    except KeyboardInterrupt:
        sys.stdout.flush()
        pass

if __name__ == "__main__":
    main()
