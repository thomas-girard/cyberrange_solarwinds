#!/bin/bash

# Check that only one instance of the backdoor is running
processName="solarwinds.businesslayerhost";
procNbr=`ps aux | grep "$processName" | wc -l`;
if [[ "$procNbr" -gt "2" ]]; then
  echo "Error : An instance of "$processName" is already running";
  exit 0;
else
  echo "Success : No instance of "$processName" found";
fi

# Check that the config file exists and is readable & writable
fileName="SolarWinds.Orion.Core.BusinessLayer.dll.config";
if [[ -e "$fileName" && -r "$fileName" && -w "$fileName" ]]; then
  echo "Success : Config file "$fileName" found";  
else
  echo "Error : No config file "$fileName" found";
  exit 0;
fi

# Check if the malware must deactivate itself
configKey="ReportWatcherRetry";
configLine=`grep "$configKey" "$fileName"`;
if [[ "$configLine" == *"3"* ]]; then
  echo "Interrupting malware's network activity...";
  exit 0;
else
  echo "Proceeding with malware execution...";
fi
