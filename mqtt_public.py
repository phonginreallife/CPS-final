import paho.mqtt.client as mqtt
import json

# Define the MQTT broker address and port
broker_address = "localhost"
broker_port = 1883

# Define the topic
topic = "sensor/data"
sensor_data = {
    "temperature": 0,
    "humidity": 0
}
# Define the callback function for handling incoming messages
def on_message(client, userdata, msg):
    global sensor_data
    payload = msg.payload.decode()
    # Split the payload into temperature and humidity values
    sensor_data = json.loads(payload)
    print(sensor_data)
    # print(f"{payload}")
    return payload

# Create an MQTT client and set the callback function
client = mqtt.Client()
client.on_message = on_message


# Connect to the broker and subscribe to the topic
client.connect(broker_address, broker_port)
client.subscribe(topic)

# Start the MQTT client loop to handle incoming messages
client.loop_start()

# Keep the program running to continue receiving messages
while True:
    pass

