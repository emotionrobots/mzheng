import paho.mqtt.client as mqtt
import json

client = mqtt.Client("python_publish")
client.connect("52.43.181.166")
topic = "toServer/cell"

#client.publish(topic, "Hello there")

testDictionary = {
    "value1": "cool stuff",
    "value2": "52.43.181.166",
    "value3": "3 meters",
    "value4": 3

}

jsonString = json.dumps(testDictionary)

#print("Hello There")
#print(jsonString)

client.publish(topic, jsonString)



