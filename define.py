
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import paho.mqtt.publish as publish


# Define the MQTT broker address and port
broker_address = "localhost"
broker_port = 1883
# Define input variables
temperature = ctrl.Antecedent(np.arange(15, 31, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(55, 71, 1), 'humidity')

# Define output variable
fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')

# Define membership functions for temperature
temperature['cold'] = fuzz.trimf(temperature.universe, [15, 15, 20])
temperature['moderate'] = fuzz.trimf(temperature.universe, [15, 20, 25])
temperature['hot'] = fuzz.trimf(temperature.universe, [20, 25, 30])

# Define membership functions for humidity
humidity['low'] = fuzz.trimf(humidity.universe, [55, 55, 60])
humidity['moderate'] = fuzz.trimf(humidity.universe, [55, 60, 65])
humidity['high'] = fuzz.trimf(humidity.universe, [60, 65, 70])

# Define membership functions for fan speed
fan_speed['off'] = fuzz.trimf(fan_speed.universe, [0, 0, 20])
fan_speed['low'] = fuzz.trimf(fan_speed.universe, [0, 20, 40])
fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [20, 60, 100])
fan_speed['high'] = fuzz.trimf(fan_speed.universe, [60, 100, 100])

# Define fuzzy rules
rule1 = ctrl.Rule(temperature['cold'] & humidity['low'], fan_speed['off'])
rule2 = ctrl.Rule(temperature['cold'] & humidity['moderate'], fan_speed['low'])
rule3 = ctrl.Rule(temperature['cold'] & humidity['high'], fan_speed['low'])
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
        topic = "fan/speed"
        message = output_value
        # Publish the message to the broker
        publish.single(topic, message, hostname=broker_address, port=broker_port)
        print('Fan Speed:', output_value)
        return output_value  