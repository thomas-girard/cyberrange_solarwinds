## Perform different checks on the environment of the malware
import psutil
from psutil import AccessDenied

# Check that only one instance of the backdoor is running
def processChecking(processName):
    count = 0
    # List processes
    for p in psutil.process_iter():
        try :
            if processName in p.name() or processName in ' '.join(p.cmdline()):
                count += 1
        except AccessDenied :
            pass
    # Check if more than 1 instance of processName is running
    if count >= 2:
        print("Error : An instance of " + processName + " is already running\n")
        input("Press enter to exit...")
        exit(1)
    print("Success : No instance of " + processName + " found\n")
    return 0


if __name__ == "__main__":
    processName = "solarwinds.businesslayerhost"
    processChecking(processName)

    input("Press enter to exit...")