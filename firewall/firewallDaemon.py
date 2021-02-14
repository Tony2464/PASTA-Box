import getIpAdresses
import json
import datetime
from os import listdir, walk
from os.path import isfile, join
from crontabs import Cron, Tab


# Return false if the ip addresses rules are outdated

def isOutdated(mode, duration, nbDays):
    if mode == 1:
        return (30 * int(duration)) > int(nbDays)
    else:
        return (7 * int(duration)) > int(nbDays)


# Date substraction between current date and the config.json

def subDate(dateConfig):
    current = datetime.datetime.now()
    dateConfigArray = dateConfig.split("/")
    dateConfigObject = datetime.datetime(
        int(dateConfigArray[2]), int(dateConfigArray[1]), int(dateConfigArray[0]))
    return current - dateConfigObject


###### Beginning of the program ######

config = "config.json"
with open(config, encoding="utf8", errors="ignore") as configFile:
    configData = configFile.read()
    configFile.close()
jsonData = json.loads(configData)
sub = subDate(jsonData["LastFetch"])

if(isOutdated(jsonData["Mode"], jsonData["Duration"], sub.days) == False):
    getIpAdresses.fetchIP()

if jsonData["Mode"] == "1":  # Monthly job
    Cron().schedule(
        Tab(name="fetchIP")
        .every(months=int(jsonData["Duration"]))
        .run(getIpAdresses.fetchIP)
    ).go()
elif jsonData["Mode"] == "2":  # Weekly job
    Cron().schedule(
        Tab(name="fetchIP")
        .every(weeks=int(jsonData["Duration"]))
        .run(getIpAdresses.fetchIP)
    ).go()
