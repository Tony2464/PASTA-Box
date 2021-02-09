import getIpAdresses
import json
from datetime import datetime
from os import listdir, walk
from os.path import isfile, join
from crontabs import Cron, Tab

###### Beginning of the program ######

config = "config.json"
with open(config, encoding="utf8", errors="ignore") as configFile:
    configData = configFile.read()
    configFile.close()

jsonData = json.loads(configData)
if jsonData["Mode"] == "1": # Monthly job
    Cron().schedule(
        Tab(name="fetchIP")
        .every(months=int(jsonData["Duration"]))
        .run(getIpAdresses.fetchIP)
    ).go()
elif jsonData["Mode"] == "2": # Weekly job
    Cron().schedule(
        Tab(name="fetchIP")
        .every(weeks=int(jsonData["Duration"]))
        .run(getIpAdresses.fetchIP)
    ).go()
else:
    Cron().schedule(
        Tab(name="fetchIP")  # Daily job
        .every(days=int(jsonData["Duration"]))
        .run(getIpAdresses.fetchIP)
    ).go()

#fetchIP()
