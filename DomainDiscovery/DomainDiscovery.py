import winreg
import sys

path = winreg.HKEY_CURRENT_USER

def read_reg(k):
    try:
        key = winreg.OpenKeyEx(path, r"Volatile Environment\\")
        value = winreg.QueryValueEx(key,k)
        if key:
            winreg.CloseKey(key)
        return value[0]
    except Exception as e:
        print(e)
    return None

def main():
    domain = read_reg('USERDOMAIN')
    print("The current domain is " + str(domain) + "\n")

    prohibitedList = ['SOLARWINDS','Solarwinds','solarwinds','SolarWinds']

    for k in prohibitedList:
        if k in domain:
            print("This domain belongs to Solarwinds and should not be targeted\n")
            return 1
        else:
            print("All good, we can continue\n")
            return 0

if __name__ == "__main__":
    main()
    sys.exit(0)