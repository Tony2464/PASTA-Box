# Conf file for trafic capture and insertion

import sys
sys.path.append("..")
from secret import secret

# CAPTURE
interface = "br0"
bufferSize = "200"  # Put 0 for default's Tshark value (2 Mb)

# DATABASE
dbConfig = {}
dbConfig["user"] = secret.dbLogin
dbConfig["password"] = secret.dBpassword
dbConfig["host"] = "127.0.0.1"
dbConfig["port"] = 3306
dbConfig["database"] = "pastadb"
