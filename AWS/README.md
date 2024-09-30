# Peekabot AWS Integration and Live Feed

## Overview

The **Peekabot Project** is a robotic system designed to autonomously follow or avoid users based on visual cues. To enhance control and monitoring, we have integrated **AWS IoT** for secure command and communication handling, and **ngrok** for creating a **live video feed** that can be accessed through the custom subdomain: `peekabot.uverma.com`.

### Components

1. **AWS IoT Core**:
   - Used for secure, scalable communication between the **Raspberry Pi** and other devices.
   - Enables sending and receiving commands for the robot in real-time, facilitating cloud-based control.

2. **ngrok Live Feed**:
   - Provides a **live camera feed** for remote viewing.
   - The live video stream is hosted at a custom subdomain: [peekabot.uverma.com](https://peekabot.uverma.com).
   - This allows real-time monitoring of the robot's environment and movements.

## Intended Use

- **AWS IoT** is used to enable secure, scalable command communication to the **Raspberry Pi** and **Arduinos**. This allows control from anywhere in the world using AWS's secure infrastructure.
- **ngrok** is used to set up a **live video stream** from the robot's camera, making it easy to remotely view what the robot sees.
- These services are intended to enhance the overall system by allowing:
  - **Remote command control** using AWS IoT.
  - **Remote video monitoring** through a browser accessible via the custom subdomain.

## Setup Instructions

### AWS IoT Core Setup

1. **Create an AWS Account**:
   - If you don't have one already, sign up at [AWS](https://aws.amazon.com/).

2. **Set Up AWS IoT Core**:
   - Go to the **AWS IoT Core** console.
   - **Create a Thing**: This represents your Peekabot in AWS.
   - **Attach Certificates**: AWS IoT requires secure communication using **X.509 certificates**.
   - **Policies**: Set up an **IoT policy** to define what permissions your Thing has (e.g., sending telemetry data, receiving commands).

3. **Download Certificates**:
   - Download the **root CA**, **certificate**, and **private key** when setting up your IoT Thing.
   - These files will be used to authenticate the **Raspberry Pi** when it connects to **AWS IoT**.

4. **Install AWS SDK for Python**:
   - On the **Raspberry Pi**, install the **AWS IoT Device SDK for Python**:

   ```bash
   pip install awsiotsdk
   ```

5. **Connect the Raspberry Pi**:
   - Use the downloaded certificates to securely connect to **AWS IoT**.
   - **pi_main.py** is responsible for connecting the **Raspberry Pi** to **AWS IoT**, allowing it to receive commands and send telemetry.

6. **Configuring AWS Endpoint**:
   - In the `pi_main.py` script, update the AWS endpoint URL, certificate paths, and security settings as necessary to ensure a proper connection.

### Ngrok Live Feed Setup

1. **Install ngrok**:
   - Download and install **ngrok** on the **Raspberry Pi** from [ngrok's website](https://ngrok.com/download).

2. **Setup ngrok Authentication**:
   - Set up **ngrok** with your authentication token:

   ```bash
   ngrok authtoken YOUR_NGROK_AUTH_TOKEN
   ```

3. **Create a Live Stream**:
   - Use **ngrok** to expose the **HTTP server** running on the **Raspberry Pi**:

   ```bash
   ngrok http 5000
   ```

   - Replace `5000` with the actual port number of the server hosting the live feed.

4. **Custom Domain**:
   - The live feed is accessible via a custom subdomain: [peekabot.uverma.com](https://peekabot.uverma.com).
   - This is set up by configuring **ngrok** to use the subdomain, providing easy access to view the robot's live feed remotely.

5. **Integration with Raspberry Pi**:
   - The **Raspberry Pi** runs the live feed server that can be accessed via **ngrok**.
   - Ensure that the live feed is continuously running to provide uninterrupted access.

### Running the Live Feed and IoT Communication

1. **Start the Live Feed**:

   - To start the live feed, run the following command on your **Raspberry Pi**:

   ```bash
   ngrok http 5000
   ```

   - This command will make the **camera feed** accessible through the public URL: [peekabot.uverma.com](https://peekabot.uverma.com).

2. **Start Robot Control via AWS IoT**:

   - Run **pi_main.py** to connect to **AWS IoT** and control the robot:

   ```bash
   python pi_main.py
   ```

   - This script will connect to **AWS IoT** using the configured **certificates** and **endpoint** and allow remote control via AWS.

### Project Workflow

1. **Command Sending via AWS IoT**:
   - Commands are sent to the **Raspberry Pi** using the **AWS IoT Core**.
   - The **Raspberry Pi** processes these commands and sends motor control signals to the **Arduinos** to move the robot.

2. **Live Video Stream**:
   - The **camera feed** on the **Raspberry Pi** is streamed via **ngrok**.
   - The live feed can be accessed through [peekabot.uverma.com](https://peekabot.uverma.com) to monitor the robot's actions.

3. **Robot Movement**:
   - The **Arduinos** control the robot's motors based on commands received from the **Raspberry Pi**.
   - The **Raspberry Pi** ensures commands are executed in response to the AWS IoT signals and camera feedback.

## Security Considerations

- **AWS IoT Security**:
  - Ensure that only authorized users/devices can connect to the **AWS IoT Core** by managing **certificates** and **policies**.
  - Regularly rotate the **private keys** and keep them secure.

- **Ngrok Access**:
  - Limit the exposure of the live feed by managing **ngrok** sessions properly.
  - Consider password-protecting or adding authentication to the live stream.

## Troubleshooting

1. **Unable to Connect to AWS IoT**:
   - Double-check the **AWS endpoint**, **certificates**, and **policy permissions**.
   - Use the **AWS IoT test console** to debug connections.

2. **Ngrok Not Connecting**:
   - Ensure **ngrok** is installed correctly and the authentication token is set.
   - Verify the **port number** that is being exposed matches the port on which the live feed server is running.

3. **Live Feed Delays or Drops**:
   - Verify the **network speed** on the **Raspberry Pi**.
   - Check **ngrok** logs for any connection issues.

## License

This project is open-source and available under the **GNU License**.

---

### Summary

- This README provides guidance on setting up **AWS IoT** and **ngrok** for the **Peekabot Project**.
- **AWS IoT** is used for secure command and communication handling to/from the robot.
- **Ngrok** is used to expose the robot's **live video feed** on a custom subdomain for easy remote access.
- The project aims to provide **real-time monitoring** and **remote control** capabilities, enabling the Peekabot to be operated and observed from virtually anywhere.

This README helps users understand the role of **AWS IoT** and **ngrok** in the project, their intended usage, and how to properly set up and use these components.