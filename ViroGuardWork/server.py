import paho.mqtt.client as paho
import json


def on_message(client, userdata, message):
    if message.topic == "/userRegistration" :
        new_device_info = json.loads(message.payload)
        #device_info_list.append(new_device_info)
        print("userRegistraction:") #for testing purposes
        print(new_device_info)
    elif message.topic == "/socialContact" :
        new_cell_info = json.loads(message.payload)
        #device_cell_list.append(new_cell_info)
        print(new_cell_info) #for testing purposes

def get_device_info(major, minor):
    for device in device_info_list:
        if device.get("Major") == major and device.get("Minor") == minor:
            return device

def broadcast(message):
    client.publish("broadcast", message)

def message(uuid, major, minor, message):
    topic = str(uuid)+"/"+str(major)+"/"+str(minor)
    client.publish(topic, message)

device_info_list = []
device_cell_list = []

client = paho.Client("emotioneering_beacon_server_test")
client.connect("52.43.181.166")

client.subscribe("/userRegistration")
client.subscribe("/socialContact")
client.on_message = on_message
client.loop_forever()


