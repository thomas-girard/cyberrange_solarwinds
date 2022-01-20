#!/bin/bash

# Check that only one instance of the backdoor is running
processName="solarwinds.businesslayerhost";
procNbr=`ps aux | grep "$processName" | wc -l`;
if [ "$procNbr" -gt "2" ]; then
  echo "Error : An instance of "$processName" is already running";
  exit 0;
  else
  echo "Success : No instance of "$processName" found";
fi

# Check that the config file exists
fileName="SolarWinds.Orion.Core.BusinessLayer.dll";
fileExist=`ls -la | grep "$fileName" | wc -l`;
if [ "$fileExist" -lt "1" ]; then
  echo "Error : No config file "$fileName" found";
  exit 0;
  else
  echo "Success : Config file "$fileName" found";
fi
