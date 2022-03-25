import sys, os
import glob
import requests

configName = 'updateOrion.conf'

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
        IPOrion = line[15:-1]
        pass
    if 'path' in line:
        path = line[7:-1]
        pass
    if 'url' in line:
        url = line[6:-1]
        pass
    if 'filename' in line:
        fname = line[11:-1]
        pass

url = url
r = requests.get("http://" + IPOrion + url)
open(path + fname , 'wb').write(r.content)

sys.exit(0)
