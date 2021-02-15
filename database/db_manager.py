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

        try:
            self.conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            return None
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    def cur(self):
        return self.conn.cursor()

    def queryGet(self, query, params):
        cur = self.cur()
        cur.execute(query, params)
        data = cur.fetchall()
        return data

    def queryInsert(self, query, params):
        # conn = self.conn
        cur = self.cur()
        cur.execute(query, params)
        self.conn.commit()
        return 0
