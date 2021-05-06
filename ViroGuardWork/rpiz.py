import paho.mqtt.client as paho
import json
import os,sys
sys.path.append(os.path.abspath('/home/pi/PiBeaconTracker/BLE-Beacon-Scanner/.'))
import json
import ScanUtility
import bluetooth._bluetooth as bluez
import datetime

device_info = {
  "uid": "4386-13124", #major-minor
	"name": "Michael Zheng",
	"phone": None,
  "email": None,
  "org": None
}

def on_message(client, userdata, message):
    if message.topic == "broadcast" :
        print("received broadcast")
        #react correspondingly to the instruction
        #print(device_info_list)
    elif message.topic == "uuid/major/minor" :
        print("received private message")
        #react correspondingly to the instruction

client = paho.Client(str(device_info["uid"]))
client.connect("52.43.181.166")

client.on_message = on_message

#documents whether the device have registered or not
infoSent = False 

#sends the device info to the server
if not infoSent:
  client.publish("/userRegistration", json.dumps(device_info))
  infoSent = True

#Set bluetooth device. Default 0.
dev_id = 0
try:
  sock = bluez.hci_open_dev(dev_id)
except:
  print ("Error accessing bluetooth")

ScanUtility.hci_enable_le_scan(sock)

#Scans for iBeacons
try:
  while True:
    beaconList = ScanUtility.parse_events(sock, 10)
    for beacon in beaconList:
      if beacon['type'] == 'iBeacon': 
        if beacon['uuid'] == '2f234454-cf6d-4a0f-adf2-f4911ba9ffa6':
          info = {}
          info['uid'] = device_info['uid']
          info['targetUID'] = str(beacon['major'])+'-'+str(beacon['minor'])
          info['time'] = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
          
          #enviornmental constant
          n = 2

          txPwr = int(str(~(int("{0:02b}".format(int(beacon['txPower'],16))))+1),2)
          distance = 10**((txPwr-int(beacon['rssi']))/(10*n))
          if distance<=6:
            client.publish("/socialContact", json.dumps(info))

except KeyboardInterrupt:
    pass


client.loop_forever()
