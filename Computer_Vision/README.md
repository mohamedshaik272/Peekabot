### README.md

---

# Peekabot Project

## Overview

The **Peekabot Project** is a robotic system designed to autonomously follow or avoid users based on visual cues. The project leverages **computer vision** to detect human poses and translate these into movement commands for a **robot** controlled by **two Arduinos** (one for each side of the robot). The following components are used:

- **Main Computer (with a camera)**: Runs pose detection using `main.py` and `distance_estimator.py`.
- **Raspberry Pi**: Runs `pi_main.py` to send movement commands to the Arduinos.
- **Two Arduinos**: Control the left and right wheels of the robot based on received commands.

## Components

1. **`main.py`**: This script performs **pose detection** using a camera connected to your computer. It calculates the appropriate movement commands for the robot based on the position and size of the detected person.
2. **`distance_estimator.py`**: A utility file used by `main.py` to estimate the distance of the detected person and determine the appropriate commands.
3. **`pi_main.py`**: Designed specifically for the **Raspberry Pi**, this script handles pose detection while also sending serial commands to two separate Arduinos for motor control.

### Intended Use

- **`main.py` and `distance_estimator.py`**:
  - These scripts can be used on **any machine** equipped with a camera (such as a laptop or a desktop).
  - They detect human poses in the camera feed and generate **movement commands** in **bit form** along with human-readable descriptions.
  - These scripts are intended for **testing** and **debugging** the pose detection and distance estimation algorithms in environments that may or may not involve the Raspberry Pi.

- **`pi_main.py`**:
  - This script is designed to run specifically on a **Raspberry Pi** that is connected to two **Arduino boards**.
  - It performs **pose detection** and **distance estimation** and then sends appropriate **motor control commands** to the Arduinos over serial communication.
  - The commands sent to the Arduinos are used to control the left and right wheels of the robot.
  - The intended use of `pi_main.py` is to serve as the **central controller** for a robotic system that needs to react to visual cues in real-time.

## Setup Instructions

### Requirements

- **Hardware**:
  - A computer (laptop/desktop) with a **camera**.
  - **Raspberry Pi** with two **Arduino** boards.
  - A **robotic chassis** with **motors** connected to the Arduino boards.

- **Software**:
  - **Python 3** with the following packages:
    - **OpenCV** (`cv2`)
    - **MediaPipe** (`mediapipe`)
    - **pyserial** (for serial communication on Raspberry Pi)
  - **Arduino IDE** for programming the Arduino boards.

### Installation

1. **Install Python Packages**:

   On your **main machine** or **Raspberry Pi**, install the required packages by running:

   ```bash
   pip install opencv-python mediapipe pyserial
   ```

2. **Upload Arduino Code**:

   - Use the **Arduino IDE** to upload the provided Arduino code (`arduino1.ino` and `arduino2.ino`) to each of the two Arduino boards.
   - **Arduino 1** controls the **left wheels**.
   - **Arduino 2** controls the **right wheels**.

### Running the Project

1. **Pose Detection on a Computer**:

   - To test the pose detection on your **laptop** or **desktop**:
     - Run `main.py` using a connected camera.
     - This will provide feedback on the detected human pose, including **command bits** and a **textual description** of the robot's intended actions.

   ```bash
   python main.py
   ```

2. **Pose Detection and Robot Control on Raspberry Pi**:

   - On the **Raspberry Pi**, you can run `pi_main.py` to control the robot autonomously.
   - This script will send commands to the **Arduinos** to control the left and right wheels.

   ```bash
   python pi_main.py
   ```

### Project Flow

1. **Pose Detection**:
   - The camera feed is processed using **MediaPipe** to detect human poses.
   - Bounding boxes are drawn around detected individuals to calculate movement instructions.

2. **Distance and Direction Calculation**:
   - The `DistanceEstimator` class in `distance_estimator.py` calculates the relative position and distance of the person to generate commands such as:
     - `go forward`
     - `go back`
     - `turn left`
     - `turn right`
     - `stay`
     - `target out of range`
   - Commands are generated as **bit signals** for efficient communication.

3. **Command Execution**:
   - **`pi_main.py`** sends these **bit commands** to the **Arduinos** using **serial communication**.
   - **Arduino 1** and **Arduino 2** control the **left** and **right wheels** respectively based on the commands they receive.

### Command Mapping

Commands are represented as bits for efficient communication. Each bit represents a specific action:

- **Bit 0** (`1`): Go forward
- **Bit 1** (`2`): Go back
- **Bit 2** (`4`): Turn left (Arduino 1 moves backward, Arduino 2 moves forward)
- **Bit 3** (`8`): Turn right (Arduino 1 moves forward, Arduino 2 moves backward)
- **Bit 4** (`16`): Target out of range (keep spinning in the last recorded direction)
- **Bit 7** (`128`): Stay (stop)

### Example Output

When running `main.py`, you will see console output that includes both the **bit representation** and a **textual description** of the command:

```
Command as bits: 0b101 | Description: go forward, turn left
```

This means the robot should **move forward** and **turn left**, where `0b101` is the binary representation with bits **0** (`go forward`) and **2** (`turn left`) set.

## Troubleshooting

1. **Pose Detection Issues**:
   - Ensure that the **camera** is functioning properly and is positioned such that the full body of the subject is visible.
   - Make sure you have installed **MediaPipe** and **OpenCV** correctly.

2. **Serial Communication Problems**:
   - Check that the **Raspberry Pi** is correctly connected to the **Arduinos** using proper **serial ports** (`/dev/ttyACM0`, `/dev/ttyACM1`).
   - Ensure that each **Arduino** is programmed with the correct code (`arduino1.ino` for left wheels, `arduino2.ino` for right wheels).

3. **Robot Movement Not Correct**:
   - Verify that the **motors** are wired correctly to the appropriate **motor driver pins** on the Arduinos.
   - Make sure that the **commands** being received by the Arduinos match the intended actions, as displayed by the `main.py` script.

## License

This project is open-source and free to use under the **GNU License**.

## Contributing

Feel free to contribute to this project by opening an issue or submitting a pull request.

---

### Summary:

- **`main.py`** and **`distance_estimator.py`** can be run on any computer with a **camera** to test and visualize the robot's decision-making process.
- **`pi_main.py`** is designed for the **Raspberry Pi** to perform real-time **pose detection** and send commands to the **Arduinos** to control the robot.
- The **Arduinos** execute the movement commands, allowing the robot to autonomously respond to visual cues detected by the **camera**.

This documentation provides a clear guide on the intended use, setup, and troubleshooting steps for each component in your robotic project.