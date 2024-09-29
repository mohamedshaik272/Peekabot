### README.md

---

# Peekabot: Your Intelligent Home Safety Companion

**HackOverflow 2024 Project**

## Overview

Peekabot is an innovative, cloud-connected robot that revolutionizes home safety. Built on Arduino and Raspberry Pi platforms, it utilizes advanced motion tracking technology to monitor your home environment. Peekabot provides real-time alerts for various scenarios, from child safety to elderly care and home security.

## Key Features

- **Advanced Motion Tracking**: Utilizes state-of-the-art technology to track movement of people and objects in real-time.
- **Instant Alerts**: Sends immediate text notifications for critical situations (e.g., toddler in danger, elderly falls, potential intruders).
- **Multi-Purpose Design**: Adaptable for child monitoring, elderly care, and home security.
- **Remote Access**: Cloud connectivity allows you to check on your home from anywhere.

## Technical Specifications

- **Hardware**: 
  - Arduino Uno R3
  - Raspberry Pi 4
  - 4 motors for mobility
  - Circuit board for integration

- **Software**:
  - OpenCV and Mediapipe
  - Local web server for remote access
  - Cloud-based alert system via AWS IoT

## Project Structure

The project is divided into multiple components to manage different functionalities and hardware integrations:

### Folder Structure

### [**Arduino**](Arduino)
Contains the code for the two Arduino boards that control the **left** and **right wheels** of Peekabot.

- **Arduino_1.ino**: Code to control the **left wheels** of the robot. This script receives commands from the **Raspberry Pi** to move the left motors accordingly.
- **Arduino_2.ino**: Code to control the **right wheels** of the robot. Similar to Arduino 1, this script moves the right wheels based on commands received.
- **README.md**: Documentation for setting up and using the Arduino boards in the Peekabot project.

### [**AWS**](AWS)
Contains documentation and configuration information for setting up **AWS IoT** and **ngrok** for the Peekabot project.

- **README.md**: Details how to configure AWS IoT Core for secure command and communication handling. It also includes steps to set up **ngrok** for live video streaming accessible through the subdomain [peekabot.uverma.com](https://peekabot.uverma.com).

### [**Computer_Vision**](Computer_Vision)
This folder includes the computer vision code that allows the robot to detect and track human movements.

- **distance_estimator.py**: A utility script used to calculate the distance of detected individuals from the camera. It helps determine whether the robot should move forward, backward, or stay.
- **main.py**: A general-purpose script that can be used on any machine with a camera (e.g., a laptop or desktop) to run the pose detection and generate movement commands. It displays both **bit representations** and **text descriptions** of the detected commands for easy debugging.
- **pi_main.py**: Specifically designed to run on the **Raspberry Pi**, this script connects to **AWS IoT** to receive commands and uses the **camera feed** to control the **robot's movement** in real-time. It communicates with the Arduinos to execute the movement instructions.

## How Peekabot Works

1. **Environment Scanning**: Continuously monitors the designated area using advanced sensors.
2. **Data Processing**: Analyzes collected data in real-time using **Mediapipe** to identify potential risks or unusual activities.
3. **Alert Generation**: Instantly creates and sends text alerts via **AWS IoT** when predefined safety thresholds are crossed.
4. **Remote Monitoring**: Users can check in and control Peekabot from anywhere via a secure web interface, accessible through **ngrok** at [peekabot.uverma.com](https://peekabot.uverma.com).

## Use Cases

| Scenario | Application |
|----------|-------------|
| Child Safety | Alerts parents if toddlers enter unsafe areas |
| Elderly Care | Detects falls and sends emergency notifications |
| Home Security | Monitors for intruders and can alert authorities |

## AWS IoT and Live Feed Integration

Peekabot utilizes **AWS IoT Core** to handle communication between the **Raspberry Pi**, **Arduinos**, and other devices. This integration allows for:

- **Remote Control**: Sending commands securely from the cloud to the robot.
- **Cloud-Based Alerts**: Instant alert generation when the robot detects unusual activity.

The **ngrok** live feed provides a **real-time video stream** of the robot's camera feed, which can be accessed through the subdomain [peekabot.uverma.com](https://peekabot.uverma.com). This feature allows users to monitor the robot's environment and activities from anywhere.

### Steps to Set Up AWS IoT

- **Create an IoT Thing**: Set up your device in the **AWS IoT Core** dashboard.
- **Attach Certificates**: Download and attach the necessary certificates to ensure secure communication.
- **Configure Endpoint**: Use the AWS endpoint in `pi_main.py` to connect your **Raspberry Pi** to the **AWS IoT** platform.

### Steps to Set Up ngrok

- Install **ngrok** on the **Raspberry Pi**.
- Run **ngrok** with the command:

  ```bash
  ngrok http 5000
  ```

- The live stream is hosted at [peekabot.uverma.com](https://peekabot.uverma.com) for remote viewing of the camera feed.

## Future Enhancements

- **AI-Powered Predictive Alerts**: Use AI algorithms to predict and notify users of potential risks before they occur.
- **Smart Home Integration**: Seamlessly connect with other IoT devices for a comprehensive home automation experience.
- **Customizable Behavior Patterns**: Allow users to define specific monitoring rules tailored to their unique needs.

## Live Demo

Experience Peekabot in action! Scan the QR code below to access our live demo from your smartphone. Receive real-time updates and interact with Peekabot's interface to explore its capabilities.

<img src="https://i.imgur.com/HDhXqpg.png" alt="Peekabot Demo QR Code" width="100" height="100">

## License

This project is open-source and available under the **GNU License**.

## Contributing

Feel free to contribute to this project by opening an issue or submitting a pull request.

---

*Peekabot: Keeping an eye on what matters most, so you don't have to.*