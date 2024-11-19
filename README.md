# QA_tools
The porpoise of this repository is to help QA team with regular execution by saving some time with python scripts to setup the device
for different scenarios

## Description
During regular excecution is necessary to constantly change the apk, push files such as xml or json as well as erase some data from DUT,
in this repository you will find some of the most common scenarios looking forward to keep adding more scripts

## Dependencies 
Python 3.12 for windows https://www.python.org/downloads/

## Tools and how to execute
Before trying to execute any script be sure to add the main folder to your PATH system variable
### soaInstaller.py 
This script is meant to install any SOA version either SOAA or SOAB taking into a count the versions for SAT and MARS setup
- _soaInstaller.py <soaa-sat, soaa-mars, soab-mars, soab-sat> <path to file's folder>_
  - Example: _soaInstaller.py soaa-sat C:\Users\User-Name\Desktop\SOAA14.5.23_
  - _soaInstaller.py --help or -h_ will show you the valid inputs
  - **NOTE: for this script to work as expected you must have your apks separated by version in one folder for example
      folder for SOAB 14.7.21 should contain**
      - full-userdebug.apk for MARS
      - fullNoHal-userdebug.apk for SAT
      - oemoverlay-bmw-debug.apk
      - CARMEDIA.12.0.2-0ac5fbb-release-signed.apk

### script.py
This script is meant to execute .bat files as well as install and erase xml/json files
- _script.py <name.bat, name.xml, name.json>_
  - Example execute a .bat file: _script.py quickStart.bat_
  - Example to push an XML/Json file: _script.py external_config.xml_ 
  - Example to erase a file from DUT: _script.py external_config.xml -r_
  - _script.py --help or -h_ will show you the valid inputs

### InMotion.py
This script will enable and disable the InMotion mode for RPI
- _inMotion.py <-m, -p>_
  - Exaple to park _inMotion.py -p_
  - Example to start moving _inMotion.py -m_
- **NOTE: for this script to work as expected you must have _C:\vhal_cli-1.0.1\bin_ in PATH system variable**
 
