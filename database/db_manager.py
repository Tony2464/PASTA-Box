# For db connection

import mariadb
import sys


class DbManager:
    conn = 0

    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def connect(self):
        try:
            conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            return conn
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    def cursor(self):
        return self.connect().cursor()

    def queryGet(self, query, params):
        cur = self.cursor()
        cur.execute(query, params)
        data = cur.fetchall()
        return data

    def queryInsert(self, query, params):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(query,params)
        conn.commit()
        return 0
