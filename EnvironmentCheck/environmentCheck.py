## Perform different checks on the environment of the malware
import psutil
from psutil import AccessDenied
import sys, os


def processChecking(processName):
    count = 0
    # List processes
    for p in psutil.process_iter():
        try:
            if processName in p.name() or processName in ' '.join(p.cmdline()):
                count += 1
        except AccessDenied:
            pass
    # Check if more than 1 instance of processName is running
    if count >= 2:
        print("Error : An instance of " + processName + " is already running\n")
        input("Press enter to exit...")
        exit(1)
    print("Success : No instance of " + processName + " found\n")
    return 0


def getConfigFile(configName, configKey):
    # Get absolute path
    if getattr(sys, 'frozen', False):
        path = sys._MEIPASS
    else:
        path = os.path.dirname(os.path.abspath(__file__))
    # Check if config file exists in ./ or ../ and is readable/writable
    try:
        file = open(path + "\\" + configName, "r+")
    except:
        try:
             file = open(path + "\\..\\" + configName, "r+")
        except:
            print("Error : No config file " + configName + " found or the file is not readable/writable\n")
            input("Press enter to exit...")
            exit(1)
    print("Success : Config file " + configName + " found\n")
    # Check if config file asks for malware's interruption
    value = ""
    for line in file:
        if configKey in line:
            # Remove \n and ;
            line = line[:-2]
            # Get the value
            while line[-1] != " ":
                value = line[-1] + value
                line = line[:-1]
            # Compare the value
            if value == "3":
                file.close()
                print("Config Setup : Interrupting malware's network activity...\n")
                input("Press enter to exit...")
                exit(1)
    print("Config Setup : Proceeding with malware execution...\n")

    file.close()
    return 0



if __name__ == "__main__":
    # Check that only one instance of the backdoor is running
    processName = "solarwinds.businesslayerhost"
    processChecking(processName)

    # Check that the config file exists and is readable & writable
    # Check if the malware must deactivate itself
    configName = "SolarWinds.Orion.Core.BusinessLayer.dll.config"
    configKey = "ReportWatcherRetry"
    getConfigFile(configName, configKey)

    exit(0)