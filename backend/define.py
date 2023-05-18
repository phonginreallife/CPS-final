import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import paho.mqtt.publish as publish

# Define MQTT broker details
broker_address = "broker.emqx.io"
broker_port = 1883
mqtt_username = "emqx"
mqtt_password = "public"
mqtt_topic = "fan_speed"

# Define input variables
temperature = ctrl.Antecedent(np.arange(25, 51, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(50, 96, 1), 'humidity')

# Define output variable
fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')

# Define membership functions for temperature
temperature['cool'] = fuzz.trimf(temperature.universe, [25, 25, 37])
temperature['moderate'] = fuzz.trimf(temperature.universe, [25, 37, 50])
temperature['hot'] = fuzz.trimf(temperature.universe, [37, 50, 50])

# Define membership functions for humidity
humidity['low'] = fuzz.trimf(humidity.universe, [50, 50, 70])
humidity['moderate'] = fuzz.trimf(humidity.universe, [50, 70, 90])
humidity['high'] = fuzz.trimf(humidity.universe, [70, 90, 95])

# Define membership functions for fan speed
fan_speed['off'] = fuzz.trimf(fan_speed.universe, [0, 0, 20])
fan_speed['low'] = fuzz.trimf(fan_speed.universe, [0, 20, 40])
fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [20, 60, 100])
fan_speed['high'] = fuzz.trimf(fan_speed.universe, [60, 100, 100])

# Define fuzzy rules
rule1 = ctrl.Rule(temperature['cool'] & humidity['low'], fan_speed['off'])
rule2 = ctrl.Rule(temperature['cool'] & humidity['moderate'], fan_speed['low'])
rule3 = ctrl.Rule(temperature['cool'] & humidity['high'], fan_speed['low'])
rule4 = ctrl.Rule(temperature['moderate'] & humidity['low'], fan_speed['low'])
rule5 = ctrl.Rule(temperature['moderate'] & humidity['moderate'], fan_speed['medium'])
rule6 = ctrl.Rule(temperature['moderate'] & humidity['high'], fan_speed['medium'])
rule7 = ctrl.Rule(temperature['hot'] & humidity['low'], fan_speed['low'])
rule8 = ctrl.Rule(temperature['hot'] & humidity['moderate'], fan_speed['medium'])
rule9 = ctrl.Rule(temperature['hot'] & humidity['high'], fan_speed['high'])

# Create control system and add rules
system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
controller = ctrl.ControlSystemSimulation(system)

def process_text_input(desired_value):
    # Set input values
    controller.input['temperature'] = desired_value['temp']
    controller.input['humidity'] = desired_value['hum']

    # Compute the fuzzy logic system
    controller.compute()

    # Get the crisp output value
    output_value = controller.output['fan_speed']

    # Define the topic and message
    payload = float(output_value)

    # Publish the payload to the broker
    publish.single(mqtt_topic, payload, hostname=broker_address, port=broker_port,
                   auth={'username': mqtt_username, 'password': mqtt_password})
    return output_value
