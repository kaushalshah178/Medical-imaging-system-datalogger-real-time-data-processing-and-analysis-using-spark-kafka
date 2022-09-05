#!/usr/bin/python

'''
To generate <number> JSON data: 
$ ./iotsimulator.py <number>

'''

import sys
import datetime
import random
from random import randrange
import re
import copy


# Set number of simulated messages to generate
if len(sys.argv) > 1:
  num_msgs = int(sys.argv[1])#10
else:
  num_msgs = 1

# mapping of a guid and a state {guid: state}
device_state_map = {} 

# average annual temperature of each state
humidity_base = {'PETCT1': 48.3, 'PETCT2': 55.3, 'PETCT3': 58.5, 'PETCT4': 43.1, 
		  'PETCT5': 51.8, 'PETCT6': 70.0, 'PETCT7': 70.7, 'PETCT8': 42.0, 
		  'PETCT9': 43.8, 'PETCT10': 52.7, 'PETCT11': 53.4, 'PETCT12': 64.8, 
		  'CT1': 66.4, 'CT2': 59.0, 'CT3': 40.4, 'CT4': 48.8, 
		  'CT5': 57.6, 'CT6': 45.4, 'CT7': 48.8, 'CT8': 59.4, 
		  'CT9': 49.9, 'CT10': 55.1, 'CT11': 45.1, 'CT12': 26.6, 
		  'MRI1': 62.8, 'MRI2': 60.4, 'MRI3': 42.9, 'MRI4': 51.8, 
		  'MRI5': 63.5, 'MRI6': 51.7, 'MRI7': 47.8, 'MRI8': 59.6, 
		  'MRI9': 60.3, 'MRI10': 44.4, 'MRI11': 49.0, 'MRI12': 41.0, 
		  'SPECT1': 54.2, 'SPECT2': 47.9, 'SPECT3': 50.7, 'SPECT4': 48.6, 
		  'SPECT5': 54.5, 'SPECT6': 41.2, 'SPECT7': 44.4, 'SPECT8': 50.1, 
		  'LINAC1': 54.3, 'LINAC2': 42.7, 'LINAC3': 63.4, 'LINAC4': 62.4, 
		  'LINAC5': 55.6, 'LINAC6': 48.4, 'LINAC7': 45.2}

# latest temperature measured by sensors {guid: temperature}
current_humidity = {}

# Fixed values
guid_base = "0-ZZZ12345678-"
destination = "0-AAA12345678"
format = "urn:example:sensor:humidity"

# Choice for random letter
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

iotmsg_header = """\
{ "guid": "%s", 
  "destination": "%s", 
  "medicalimagingdevice": "%s", """

iotmsg_eventTime = """\
  "eventTime": "%sZ", """

iotmsg_payload ="""\
  "payload": {"format": "%s", """

iotmsg_data ="""\
	 "data": { "humidity": %.1f  }   
	 }
}"""


##### Generate JSON output:
if __name__ == "__main__":
	for counter in range(0, num_msgs):#10
		rand_num = str(random.randrange(0, 9)) + str(random.randrange(0, 9))#46
		rand_letter = random.choice(letters)#P
		temp_init_weight = random.uniform(-5, 5)#3
		temp_delta = random.uniform(-1, 1)#1

		guid = guid_base + rand_num + rand_letter # 0-ZZZ12345678-46P
		medicalimagingdevice = random.choice(humidity_base.keys()) #NV

		if (not guid in device_state_map): # first entry
			device_state_map[guid] = medicalimagingdevice #NV
			current_humidity[guid] = humidity_base[medicalimagingdevice] + temp_init_weight	 #52.9
			
		elif (not device_state_map[guid] == medicalimagingdevice):		# The guid already exists but the randomly chosen state doesn't match
			medicalimagingdevice = device_state_map[guid]

		humidity = current_humidity[guid] + temp_delta #53.9
		current_humidity[guid] = humidity  # update current temperature#53.9	
		today = datetime.datetime.today() #19092021110102
		datestr = today.isoformat()#19092021110102

		print re.sub(r"[\s+]", "", iotmsg_header) % (guid, destination, medicalimagingdevice),
		print re.sub(r"[\s+]", "", iotmsg_eventTime) % (datestr),
		print re.sub(r"[\s+]", "", iotmsg_payload) % (format),
		print re.sub(r"[\s+]", "", iotmsg_data) % (humidity)