import sys, os
import glob
import requests

configName = 'update.conf'

root_dir = "C:/Users/"
for filename in glob.iglob(root_dir + '**/**', recursive=True):
    if configName in filename:
        path = filename
        break
try:
    file = open(path, "r+")
except:
    print("Error : No config file " + configName + " found or the file is not readable/writable\n")
    sys.exit(1)

for line in file.readlines():
    if 'solarwindsIP' in line:
        IP = line[15:]
        pass
    if 'path' in line:
        path = line[7:]
        pass
    if 'url' in line:
        url = line[6:]
        pass
    if 'filename' in line:
        fname = line[11:]
        pass

url = url + fname
r = requests.get(url)
open(path + fname , 'wb').write(r.content)

sys.exit(0)
