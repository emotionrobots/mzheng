import paho.mqtt.client as paho
import json

  

def on_message(client, userdata, message):
  try:
    json_object = json.loads(message.payload)
  except ValueError as e:
    print(message.payload.decode("UTF-8"))

        


client = paho.Client("python_subscribe")
client.connect("52.43.181.166")
client.subscribe("my_own_topic")
client.on_message = on_message
client.loop_forever()