import serial
import time

# Initialize serial communication with both Arduinos
arduino1 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Replace with correct port for Arduino 1
arduino2 = serial.Serial('/dev/ttyACM1', 9600, timeout=1)  # Replace with correct port for Arduino 2

time.sleep(2)  # Wait for connection to establish

# Function to send command to a specified Arduino
def send_command(arduino, command):
    arduino.write((command + '\n').encode('utf-8'))  # Send command to Arduino
    time.sleep(0.1)  # Give Arduino some time to process
    if arduino.in_waiting > 0:
        response = arduino.readline().decode('utf-8').rstrip()  # Read response from Arduino
        print(response)

try:
    while True:
        # Ask user for which Arduino to control and what command to send
        target = input("Enter Arduino to control ('1' or '2', 'EXIT' to quit): ")
        
        if target.upper() == 'EXIT':
            break  # Exit the loop and end the program

        if target == '1':
            user_command = input("Enter command for Arduino 1 ('ON', 'OFF'): ")
            if user_command.upper() in ['ON', 'OFF']:
                send_command(arduino1, user_command.upper())
            else:
                print("Invalid command. Please enter 'ON' or 'OFF'.")

        elif target == '2':
            user_command = input("Enter command for Arduino 2 ('ON', 'OFF'): ")
            if user_command.upper() in ['ON', 'OFF']:
                send_command(arduino2, user_command.upper())
            else:
                print("Invalid command. Please enter 'ON' or 'OFF'.")

        else:
            print("Invalid Arduino selection. Please enter '1' or '2'.")

except KeyboardInterrupt:
    # Handle a graceful exit on a keyboard interrupt
    print("\nProgram interrupted by user.")

finally:
    arduino1.close()  # Close serial port for Arduino 1
    arduino2.close()  # Close serial port for Arduino 2