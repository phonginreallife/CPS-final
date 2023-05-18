from flask import request
import define as dfi
import paho.mqtt.client as mqtt
import json
import time
import sys


broker_address = "broker.emqx.io"
broker_port = 1883
username = "emqx"
password = "public"

# Define the topic
topic = "sensor_data"
temp = '0'
hum = '0'
output_value = 1
message = []
words = "set temperature 16 and humidity 70"
def extract_numbers(text):
    numbers = []
    words = text.split()  # Split the message string into words
    for word in words:
        try:
            number = float(word)  # Try to convert each word to a float number
            numbers.append(number)
        except ValueError:
            pass  # Ignore words that cannot be converted to numbers
    return numbers
# Define the callback function for handling incoming messages
def on_message(client, userdata, msg):
    global sensor_data
    global output_value
    global message 
    message = extract_numbers(words)
    payload = msg.payload.decode()
    # Split the payload into temperature and humidity values
    sensor_data = json.loads(payload)
    if (sensor_data['temp'] != message[0] or sensor_data['hum'] != message[1]):
            if (sensor_data['temp'] != message[0] and sensor_data['hum'] != message[1]):
                output_value = dfi.process_text_input(sensor_data)
                time.sleep(1)
    else:
         output_value = 0
    # print(f"{payload}")
    return payload
# Create an MQTT client and set the callback function
client = mqtt.Client()
client.on_message = on_message

# Set username and password
client.username_pw_set(username, password)
# Connect to the broker and subscribe to the topic
client.connect(broker_address, broker_port)
client.subscribe(topic)

# Start the MQTT client loop to handle incoming messages
client.loop_start()

# Keep the program running to continue receiving messages
while True:
    if  output_value == 0:   
         sys.exit(0)
