# Required 
# libbluetooth-dev bluez-utils

#Required imports
import bluetooth
import os
import yaml
import time
from os.path import expanduser
import logging
import signal
import sys

#Debug levek, change to INFO to see only important logging
logging.basicConfig(filename='/var/log/autolock.log',level=logging.DEBUG) 

#Initialization of variables
target_address = None
device_address = None

#Configure the sleep time
sleep_time = 3

current_time = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
home = expanduser("~")
config_file = home+"/.autolock/.secured_device"

#Function to handle Crtl+C
def signal_handler(signal, frame):
    print('=================')
    print('Execution aborted')
    print('=================')
    logging.debug('[DEBUG] ' + current_time + ' -  Execution aborted')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#Running for the first time    
logging.debug('[DEBUG] ' + current_time + ' -  Starting the program')
if os.path.exists(config_file) is False:
    os.system('mkdir ~/.autolock/ >/dev/null 2>&1')
    logging.debug('[DEBUG] ' + current_time + ' -  Config file does not exists, creating the directory')
    
    #Discover nearby bluetooth devices
    nearby_devices = bluetooth.discover_devices()
    logging.debug('[DEBUG] ' + current_time + ' -  Discovering Bluetooth devices')

    #Print nearby devices list
    for bdaddr in nearby_devices:
        print "Device Name", bluetooth.lookup_name( bdaddr )
        print "Device Address ", bdaddr
        logging.debug('[DEBUG] ' + current_time + ' -  Printing nearby devices')
    
    #Detect phone to match with
    print "Which is the name of device you want to use to authenticate?"
    print "(Remember to enable device visibility at this point)"
    target_name = raw_input()
    logging.debug('[DEBUG] ' + current_time + ' -  Authorized phone loadad')

    #Check devices MAC address
    for bdaddr in nearby_devices:
        if target_name == bluetooth.lookup_name( bdaddr ):
            target_address = bdaddr
            break
            logging.debug('[DEBUG] ' + current_time + ' -  MAC Address obtained')

    text_file = open(config_file, "w")
    text_file.write("Target Name: %s\n" % target_name)
    text_file.write("Target Address: %s\n" % target_address)
    text_file.close()
    logging.debug('[DEBUG] ' + current_time + ' -  Configuration file created')
else:
    logging.debug('[DEBUG] ' + current_time + ' -  Configuration file already existed')

secured_device = open(config_file)
dataMap = yaml.safe_load (secured_device)
secured_device.close()
target_name = dataMap["Target Name"]
target_address = dataMap["Target Address"]
logging.debug('[DEBUG] ' + current_time + ' -  Parsing YAML configuration file')

print "Device Information to Search"
print "Target Name: " + target_name
print "Target Address: " + target_address
logging.debug('[DEBUG] ' + current_time + ' -  Target Name: ' + target_name)
logging.debug('[DEBUG] ' + current_time + ' -  Target Address: ' + target_address)
logging.debug('[DEBUG] ' + current_time + ' -  Defined information to search')

while True:
    #Check if the device is near
    if target_name == bluetooth.lookup_name( target_address ):
        print "Found target bluetooth device: " + target_name
        logging.info('[INFO] '+ current_time + ' - Found target bluetooth device: ' + target_name)
        logging.debug('[DEBUG] ' + current_time + ' -  Device found, continuing with loop')
    else:
        print "Could not find target bluetooth device nearby"
        logging.debug('[DEBUG] ' + current_time + ' -  Devide not found, blocking computer')
        logging.info('[INFO] '+ current_time + ' - Could not find target bluetooth device nearby')
        os.system('gnome-screensaver-command --lock')
    time.sleep(sleep_time) 
