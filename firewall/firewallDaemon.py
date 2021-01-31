import os
from datetime import datetime
from os import listdir, walk
from os.path import isfile, join
from crontabs import Cron, Tab


def fileList(source):
    files = []
    for root, dirnames, filenames in os.walk(source):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

# Schedule a single job

def my_job(*args, **kwargs):
    #print('args={} kwargs={} running at {}'.format(args, kwargs, datetime.now()))
    res = os.system("cd blocklist-ipsets && git fetch")
    listFiles = fileList("blocklist-ipsets/")
    dataIP = []

    for i in range(len(listFiles)):
        with open(listFiles[i], encoding="utf8", errors='ignore') as IPfile:
            data = IPfile.readlines()
            IPfile.close()

        for j in range(len(data)):
            if(data[j].find("#") == -1):
                dataIP.append(data[j])

    print(len(dataIP))
    dataIP = list(dict.fromkeys(dataIP))
    print(len(dataIP))
    # for l in range(len(dataIP)):
    #     print(dataIP[l])  

# Will run with a 5 second interval synced to the top of the minute
Cron().schedule(
    Tab(name='run_my_job').every(seconds=30).run(
        my_job, 'my_arg', my_kwarg='hello')
).go()




