import os
import threading
import time


# List all the commands available

def listCmd(cmd):
    commands = {

        "restart-services": 1,
        "restart": 2,
        "shutdown": 3

    }

    return commands.get(cmd, 1)


# Get the command from the HMI

def getCmd(cmd):
    numberCmd = listCmd(cmd)
    if(numberCmd == 1):
        return -6

    t = threading.Thread(target=executeCmd, args=(numberCmd,))
    t.start()

    return 0


# Execute the command from the HMI

def executeCmd(numberCmd):
    time.sleep(5)
    os.system("sudo /PASTA-Box/settings/execute_command.sh " + str(numberCmd))
