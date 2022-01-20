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

