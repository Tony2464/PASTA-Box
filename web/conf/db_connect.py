#For db connection

import config
import mariadb
import sys

try:
    conn = mariadb.connect(
        user=config.dbConfig["user"],
        password=config.dbConfig["password"],
        host=config.dbConfig["host"],
        port=config.dbConfig["port"],
        database=config.dbConfig["database"]
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)