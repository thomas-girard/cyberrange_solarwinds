import sys, os
import glob
import requests

configName = 'updateOrion.conf'

root_dir = "C:/Users/"

print("Fetching configuration file " + configName + "...")

for filename in glob.iglob(root_dir + '**/**', recursive=True):
    if configName in filename:
        path = filename
        break
try:
    file = open(path, "r+")
except:
    print("Error : No config file " + configName + " found or the file is not readable/writable\n")
    sys.exit(1)

print("File found !\n")
print("Parsing configuration file...\n")

for line in file.readlines():
    if 'solarwindsIP' in line:
        IPOrion = line[15:-1]
        continue
    if 'path' in line:
        path = line[7:-1]
        continue
    if 'url' in line:
        url = line[6:-1]
        continue
    if 'filename' in line:
        fname = line[11:-1]
        continue

print("Downloading Orion update...\n")

r = requests.get("http://" + IPOrion + url)
open(path + fname , 'wb').write(r.content)

print("Update successfully downloaded at : " + path + fname)

sys.exit(0)
