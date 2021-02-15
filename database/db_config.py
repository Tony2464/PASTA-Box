import sys
sys.path.append("..")
from secret import secret

dbConfig = {}
dbConfig["user"] = secret.dbLogin
dbConfig["password"] = secret.dBpassword
dbConfig["host"] = "127.0.0.1"
dbConfig["port"] = 3306
dbConfig["database"] = "pastadb"
