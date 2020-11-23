import paho.mqtt.client as paho
import json
import os,sys
sys.path.append(os.path.abspath('/home/pi/PiBeaconTracker/BLE-Beacon-Scanner/.'))
import json
import ScanUtility
import bluetooth._bluetooth as bluez

device_info = {
  "UID": "4386-13124", #major-minor
	"Name": "Michael Zheng",
	"Phone": None,
  "Email": None,
  "Org": []
}

cell = [
	{
		"UUID": device_info.get("UUID"),
		"Major": device_info.get("Major"),
		"Minor": device_info.get("Minor"),
		"StartTime": None,
		"EndTime": None
	}
]

def on_message(client, userdata, message):
    if message.topic == "broadcast" :
        print("received broadcast")
        #react correspondingly to the instruction
        #print(device_info_list)
    elif message.topic == "uuid/major/minor" :
        print("received private message")
        #react correspondingly to the instruction

client = paho.Client("uuid_major_minor")
client.connect("52.43.181.166")

client.subscribe("broadcast")
client.subscribe("uuid/major/minor")

client.on_message = on_message

#sends the device info to the server
client.publish("toServer/info", json.dumps(device_info))

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
          info["Type"] = "iBeacon"
          info["Major"] = beacon['major']
          info["Minor"] = beacon['minor']
          info["Distance"] = None
          info["RSSI"] = beacon['rssi']
          info["TxPower"] = beacon['txPower']
          cell.append(info)
    client.publish("toServer/cell", json.dumps(cell))

except KeyboardInterrupt:
    pass


client.loop_forever()
