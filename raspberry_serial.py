import cv2
import mediapipe as mp
import serial
import time

# Set up frame width and height
frameWidth = 640
frameHeight = 480

# Initialize MediaPipe Pose Detection
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Use Pose with default settings
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize video capture from the default camera (usually webcam)
cap = cv2.VideoCapture(0)

# Set the frame width and height
cap.set(3, frameWidth)
cap.set(4, frameHeight)

# Check and print actual width and height
actual_width = cap.get(3)
actual_height = cap.get(4)
print(f"Actual width: {actual_width}")
print(f"Actual height: {actual_height}")

# Initialize serial communication with both Arduinos
arduino1 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Replace with correct port for Arduino 1 (left wheels)
arduino2 = serial.Serial('/dev/ttyACM1', 9600, timeout=1)  # Replace with correct port for Arduino 2 (right wheels)

time.sleep(2)  # Wait for connection to establish

# Function to send command to a specified Arduino
def send_command(arduino, command):
    arduino.write((command + '\n').encode('utf-8'))  # Send command to Arduino
    time.sleep(0.1)  # Give Arduino some time to process
    if arduino.in_waiting > 0:
        response = arduino.readline().decode('utf-8').rstrip()  # Read response from Arduino
        print(response)

# To store the previous bot command to avoid repeated commands
previous_command = None
go_forward_counter = 0  # Counter for consecutive frames where user is far away
go_forward_threshold = 3  # Number of consecutive frames to trigger "GO FORWARD" command

while cap.isOpened():
    success, img = cap.read()
    
    if success:
        # Convert the image to RGB for pose detection
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Perform pose detection
        results = pose.process(img_rgb)

        # If a pose is detected, draw the pose landmarks on the image
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
            )

            # Get the list of landmarks
            landmarks = results.pose_landmarks.landmark

            # Initialize variables to calculate the bounding box
            x_min = frameWidth
            y_min = frameHeight
            x_max = 0
            y_max = 0

            # Iterate through all the pose landmarks to find the bounding box coordinates
            for landmark in landmarks:
                x = int(landmark.x * frameWidth)
                y = int(landmark.y * frameHeight)

                # Update the min/max coordinates to include all pose landmarks
                x_min = min(x_min, x)
                y_min = min(y_min, y)
                x_max = max(x_max, x)
                y_max = max(y_max, y)

            # Add some padding to the bounding box (optional, to ensure head is fully inside the box)
            padding = 20  # Add some padding to make the box larger
            x_min = max(0, x_min - padding)
            y_min = max(0, y_min - padding)
            x_max = min(frameWidth, x_max + padding)
            y_max = min(frameHeight, y_max + padding)

            # Calculate the center of the bounding box
            box_center_x = (x_min + x_max) // 2
            box_center_y = (y_min + y_max) // 2

            # Calculate the height of the bounding box
            box_height = y_max - y_min

            # Command logic based on the bounding box position and size
            bot_command = None

            # Check if the person is too close or too far based on bounding box height
            if box_height > 280:  # Height threshold to determine if the user is too close
                bot_command = "GO BACK"
                go_forward_counter = 0  # Reset counter when person is too close
            elif box_height < 180:  # Lower height threshold to make "GO FORWARD" more sensitive
                go_forward_counter += 1
                if go_forward_counter >= go_forward_threshold:
                    bot_command = "GO FORWARD"
                    go_forward_counter = 0  # Reset after issuing command
            elif box_center_x > 450:  # Right of the frame
                bot_command = "GO RIGHT"
                go_forward_counter = 0  # Reset counter
            elif box_center_x < 200:  # Left of the frame
                bot_command = "GO LEFT"
                go_forward_counter = 0  # Reset counter
            else:
                go_forward_counter = 0  # Reset counter if no specific condition is met

            # Print the command only if it changes
            if bot_command and bot_command != previous_command:
                print(bot_command)
                previous_command = bot_command

                # Send the appropriate command to the Arduinos
                if bot_command == "GO FORWARD":
                    send_command(arduino1, "FORWARD")
                    send_command(arduino2, "FORWARD")
                elif bot_command == "GO BACK":
                    send_command(arduino1, "BACKWARD")
                    send_command(arduino2, "BACKWARD")
                elif bot_command == "GO LEFT":
                    send_command(arduino1, "BACKWARD")  # Left wheels move backward
                    send_command(arduino2, "FORWARD")  # Right wheels move forward
                elif bot_command == "GO RIGHT":
                    send_command(arduino1, "FORWARD")  # Left wheels move forward
                    send_command(arduino2, "BACKWARD")  # Right wheels move backward

            # Draw the bounding box around the detected pose
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
        else:
            # Alert if target is out of frame
            if previous_command != "ALERT: TARGET OUT OF FRAME!!!!!!":
                print("ALERT: TARGET OUT OF FRAME!!!!!!")
                previous_command = "ALERT: TARGET OUT OF FRAME!!!!!!"
                # Stop both Arduinos if the target is out of frame
                send_command(arduino1, "STOP")
                send_command(arduino2, "STOP")
            go_forward_counter = 0  # Reset counter

        # Show the result in a window
        cv2.imshow("Pose Detection with Bounding Box Including Head", img)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture object and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Close the serial ports
arduino1.close()
arduino2.close()