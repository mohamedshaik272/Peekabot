import time
import serial
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Serial setup for Arduinos
arduino1 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Replace with correct port for Arduino 1
arduino2 = serial.Serial('/dev/ttyACM1', 9600, timeout=1)  # Replace with correct port for Arduino 2

time.sleep(2)  # Wait for connection to establish

# AWS IoT settings
client_id = "RaspberryPiController"
host = "your-iot-endpoint.amazonaws.com"  # Replace with your AWS IoT endpoint
root_ca = "AmazonRootCA1.pem"
private_key = "your-private-key.pem.key"
certificate = "your-certificate.pem.crt"

# Setup AWS IoT MQTT client
myMQTTClient = AWSIoTMQTTClient(client_id)
myMQTTClient.configureEndpoint(host, 8883)
myMQTTClient.configureCredentials(root_ca, private_key, certificate)

# MQTT client configurations
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Function to send command to a specified Arduino
def send_command(arduino, command):
    arduino.write((command + '\n').encode('utf-8'))
    time.sleep(0.1)
    if arduino.in_waiting > 0:
        response = arduino.readline().decode('utf-8').rstrip()
        print(response)

# Callback when a message is received
def customCallback(client, userdata, message):
    print(f"Received message: {message.topic} -> {message.payload.decode()}")
    payload = message.payload.decode().strip()

    # Parsing the message to control specific Arduino
    if payload == "ON1":
        send_command(arduino1, "ON")
    elif payload == "OFF1":
        send_command(arduino1, "OFF")
    elif payload == "STATUS1":
        send_command(arduino1, "STATUS")
    elif payload == "ON2":
        send_command(arduino2, "ON")
    elif payload == "OFF2":
        send_command(arduino2, "OFF")
    elif payload == "STATUS2":
        send_command(arduino2, "STATUS")
    else:
        print("Unknown command received")

# Connect and subscribe to AWS IoT
myMQTTClient.connect()
myMQTTClient.subscribe("motor/control", 1, customCallback)

print("Connected to AWS IoT and subscribed to topic")

try:
    while True:
        # Keep the program running to continuously check for MQTT messages
        time.sleep(1)

except KeyboardInterrupt:
    print("Disconnecting...")
finally:
    myMQTTClient.disconnect()
    arduino1.close()
    arduino2.close()
