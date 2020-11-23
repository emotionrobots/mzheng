import paho.mqtt.client as paho
import json


def on_message(client, userdata, message):
    if message.topic == "toServer/info" :
        new_device_info = json.loads(message.payload)
        device_info_list.append(new_device_info)
        print(device_info_list) #for testing purposes
    elif message.topic == "toServer/cell" :
        new_cell_info = json.loads(message.payload)
        device_cell_list.append(new_cell_info)
        print(device_cell_list) #for testing purposes

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

client = paho.Client("emotioneering_beacon_server")
client.connect("52.43.181.166")

client.subscribe("toServer/info")
client.subscribe("toServer/cell")
client.on_message = on_message
client.loop_forever()


