#!/usr/bin/python
from conf import config
from database import db_manager
import sys
sys.path.append("..")


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

for line in sys.stdin:
    count+=1
    # dbManager.queryInsert("INSERT INTO Frame (portSource) VALUES (?)", (line.split(" ")))
    # print(line.split(","))
    # print(line)
    # frame = line
    frame = line.split(",")
    # print(frame)

    # Determine tcp port or udp port
    if frame[0]: # Tcp port
        srcport = frame[0]
        dstport = frame[1]
    else: # Udp port
        srcport = frame[2]
        dstport = frame[3]

    # Determine ipv4 or ipv6
    if frame[4]: #ipv4
        srcIp = frame[4]
        dstIp = frame[5]
    else:
        srcIp = frame[6]
        dstIp = frame[7]

    protocol = frame[10].split(":")
    
    applicationLayer = protocol[4] if len(protocol) == 5 else None

    # print(protocol[2])

    # print(srcport+" "+
    #       dstport + " " +
    #       frame[4] +" "+  # ip src
    #       frame[5] +" "+  # ip dst
    #       frame[6] +" "+  # mac src
    #       frame[7] + " " +  # mac dst
    #       str(applicationLayer) + " " +  # application layer
    #       frame[9] + " " +  # transport layer
    #       protocol[2] + " " +  # network layer
    #       frame[10]  # DNS query
    # )

    # print(str(frame[11])+ ":"+str(protocol))
    # print(srcport + dstport + srcIp + dstIp + frame[8] + frame[9] + str(applicationLayer) + str(frame[11]) + str(protocol[2]) + str(frame[12]))

    dbManager.queryInsert(
        "INSERT INTO `Frame` (`portSource`, `portDest`, `ipSource`, `ipDest`, `macAddrSource`, `macAddrDest`, `protocolLayerApplication`, `protocolLayerTransport`, `protocolLayerNetwork`, `date`, `domain`) VALUES(%s, %s, %s, %s,%s, %s, %s, %s, %s, NULL, %s)",
        (srcport,
         dstport,
         srcIp,  # ip src
         dstIp,  # ip dst
         frame[8],#mac src
         frame[9],#mac dst
         applicationLayer,#application layer
         frame[11],#transport layer
         protocol[2],#network layer
         frame[12]#DNS query
         )
    )


    print(count)
    # print(frame[0],
    #       frame[1],
    #       frame[2],
    #       frame[3],
    #       frame[4],
    #       frame[5],
    #       frame[6],
    #       frame[7]
    #       )

    # print(line.split(",")[0],
    #       line.split(",")[1],
    #       line.split(",")[2],
    #       line.split(",")[3],
    #       line.split(",")[4],
    #       line.split(",")[5],
    #       line.split(",")[6],
    #       line.split(",")[7],
    #       )

    # count += 1
    # print(count)

    # dbManager.queryInsert(
    #     "INSERT INTO `Frame` (`portSource`) VALUES(Anakin123
    #     ?)", ("1")
    # )

# print(count)
# print(type(sys.stdin))

# value=[("BonjourToi!")]


# insert information
# try:
#     cur.execute("INSERT INTO tabletest (columntest) VALUES (?)", (value))
# except mariadb.Error as e:
#     print(f"Error: {e}")

# conn.commit()

# cur.execute(
#     "SELECT * FROM tabletest")

# for columntest in cur:
#     # print(f"{columntest}")
#     print(f"la colonne contient : {columntest}")

# responses = cur.fetchall()

# for response in responses:
#     # print(f"{response}")
#     # print(type(response))
#     print(response[0])


# DELETE FROM tabletest;

# commande
# sudo tshark -B 200 -i eth1 -T fields -e ip.dst -c 100 2> /dev/null | python3 insertCapture.py
# sudo tshark -i wlan0 -c 10 -T fields -E separator=, -e ip.src -e ip.dst -e _ws.col.Protocol -e _ws.col.Info | python3 insertData.py

# sudo tcpdump -B 100000 -i eth1 -n -G 1 | python3 insertCapture.py
# -B (en Ko)
