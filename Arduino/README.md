### README.md

---

# Peekabot Arduino Control

## Overview

This directory contains the **Arduino code** for the **Peekabot Project**. The Peekabot system utilizes **two Arduinos** for controlling the **left** and **right wheels** of the robot. The Arduinos receive movement commands from a **Raspberry Pi** via **serial communication** and translate these commands into motor actions.

### Arduino Files

- **`arduino1.ino`**: Code for **Arduino 1** which controls the **left wheels** of the robot.
- **`arduino2.ino`**: Code for **Arduino 2** which controls the **right wheels** of the robot.

## Intended Use

- The Arduinos are intended to control the **robot’s movement** by interpreting **bitwise commands** sent from the **Raspberry Pi**.
- **Arduino 1** and **Arduino 2** operate independently:
  - **Arduino 1** handles the **left wheels**.
  - **Arduino 2** handles the **right wheels**.
- The commands are sent over a **serial connection** and are based on the visual cues processed by the Raspberry Pi (using `pi_main.py`).

## Setup Instructions

### Hardware Setup

1. **Wiring**:
   - Each Arduino is connected to a **motor driver** that controls the motors for either the left or the right wheels.
   - The **left wheels** are controlled by **Arduino 1**.
   - The **right wheels** are controlled by **Arduino 2**.
   - Each Arduino should be connected to the **Raspberry Pi** via **USB** for serial communication.

2. **Motor Pins**:
   - **Arduino 1 (Left Wheels)**:
     - **PWM Pin**: `3` (for motor speed control)
     - **Direction Pins**: `12` and `13`
   - **Arduino 2 (Right Wheels)**:
     - **PWM Pin**: `11` (for motor speed control)
     - **Direction Pins**: `4` and `5`

### Software Setup

1. **Install the Arduino IDE**:
   - Download and install the [Arduino IDE](https://www.arduino.cc/en/software) if you haven’t already.

2. **Upload the Code**:
   - Connect each Arduino to your computer via USB.
   - Open the **Arduino IDE**.
   - For **Arduino 1**:
     - Open the file `Arduino_1.ino`.
     - Select the correct **port** for the connected Arduino (Tools > Port).
     - Upload the code to **Arduino 1**.
   - Repeat the above steps for **Arduino 2**, using `Arduino_2.ino`.

### Commands and Logic

The Raspberry Pi sends **bitwise commands** to each Arduino that indicate how the robot should move. Below is a breakdown of the commands and their corresponding actions:

- **Bit 0 (`1`)**: **Go Forward**
  - **Arduino 1** and **Arduino 2** both move their wheels **forward**.
  
- **Bit 1 (`2`)**: **Go Backward**
  - **Arduino 1** and **Arduino 2** both move their wheels **backward**.

- **Bit 2 (`4`)**: **Turn Left**
  - **Arduino 1** (left wheels) moves **backward**.
  - **Arduino 2** (right wheels) moves **forward**.

- **Bit 3 (`8`)**: **Turn Right**
  - **Arduino 1** (left wheels) moves **forward**.
  - **Arduino 2** (right wheels) moves **backward**.

- **Bit 4 (`16`)**: **Target Out of Range** (Keep Spinning in Last Recorded Direction)
  - The robot will keep spinning in the **last known direction** to search for the target.

- **Bit 7 (`128`)**: **Stay**
  - Both **Arduino 1** and **Arduino 2** stop their motors.

## Troubleshooting

1. **Motor Not Moving**:
   - Ensure that the **motor driver** is properly wired to the **Arduino** and the **motor**.
   - Verify that the **power supply** to the motor driver is sufficient.

2. **Serial Communication Issues**:
   - Check the **connection** between the **Raspberry Pi** and the **Arduinos**.
   - Ensure that the correct **serial ports** are being used.

3. **Inconsistent Movement**:
   - Verify that the correct commands are being received by each Arduino.
   - You can use the **Serial Monitor** in the **Arduino IDE** to check the incoming commands.

## License

This project is open-source and available under the **GNU License**.

---

### Summary:

- The **Arduino code** controls the **left** and **right wheels** of the robot based on commands received from the **Raspberry Pi**.
- Each command is represented as a **bitwise signal**, allowing the robot to **move forward**, **backward**, **turn**, or **stay**.
- Ensure each Arduino is **correctly wired** and **programmed** for the robot to function as intended.