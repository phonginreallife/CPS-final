from flask import request
import define as dfi
import paho.mqtt.client as mqtt
import json
import time
import sys

broker_address = "localhost"
broker_port = 1883

# Define the topic
topic = "sensor/data"
temp = '0'
hum = '0'
output_value = 1
# Define the callback function for handling incoming messages
def on_message(client, userdata, msg):
    global sensor_data
    global output_value
    payload = msg.payload.decode()
    # Split the payload into temperature and humidity values
    sensor_data = json.loads(payload)
    message = [20,55]
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


# Connect to the broker and subscribe to the topic
client.connect(broker_address, broker_port)
client.subscribe(topic)

# Start the MQTT client loop to handle incoming messages
client.loop_start()

# Keep the program running to continue receiving messages
while True:
    if  output_value == 0:   
         sys.exit(0)
# message = [20,55]

# print(sensor_data)
# while (sensor_data['temp'] != message[0] and sensor_data['hum'] != message[1]):
#         output_value = dfi.process_text_input(sensor_data)
# print('Fan Speed:', output_value)
# def recognize():
#     # if request.method == 'POST':
#     #     data = request.get_json()
#     #     # Process POST request and return response
#     #     message = data.get('message', '')
#     #     message = message.split()
#     #     output_value = dfi.process_text_input(message)
#     message = [20,55]
#     act_message = mqtt.on_message()
#     while (act_message['temp'] != message[0] and act_message['hum'] != message[1]):
#         output_value = dfi.process_text_input(message)
#     return output_value

