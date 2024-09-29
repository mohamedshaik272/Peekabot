import cv2
import mediapipe as mp
from distance_estimator import DistanceEstimator  # Add this line

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

# Initialize DistanceEstimator
distance_estimator = DistanceEstimator(frameWidth, frameHeight)

previous_command = 0  # To store the previous bot command

# Function to convert command bits to human-readable text
def get_command_description(command):
    descriptions = []
    if command & 1:
        descriptions.append("go forward")
    if command & 2:
        descriptions.append("go back")
    if command & 4:
        descriptions.append("turn left")
    if command & 8:
        descriptions.append("turn right")
    if command & 16:
        descriptions.append("target out of range")
    if command & 128:
        descriptions.append("stay")
    
    return ", ".join(descriptions) if descriptions else "no action"

while cap.isOpened():
    success, img = cap.read()
    if success:
        # Convert the image to RGB for pose detection
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Perform pose detection
        results = pose.process(img_rgb)
        
        # Draw guide lines
        img = distance_estimator.draw_guide(img)
        
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
            x_min, y_min = frameWidth, frameHeight
            x_max, y_max = 0, 0
            
            # Iterate through all the pose landmarks to find the bounding box coordinates
            for landmark in landmarks:
                x, y = int(landmark.x * frameWidth), int(landmark.y * frameHeight)
                x_min, y_min = min(x_min, x), min(y_min, y)
                x_max = max(x_max, x)
                y_max = max(y_max, y)
            
            # Add some padding to the bounding box
            padding = 20
            x_min = max(0, x_min - padding)
            y_min = max(0, y_min - padding)
            x_max = min(frameWidth, x_max + padding)
            y_max = min(frameHeight, y_max + padding)
            
            # Get command from DistanceEstimator
            bot_command = distance_estimator.get_command(x_min, y_min, x_max, y_max)
            
            # Send command only if it is different from previous one
            if bot_command != previous_command:
                # Print the command in both bit and text form
                command_bits = bin(bot_command)
                command_description = get_command_description(bot_command)
                print(f"Command as bits: {command_bits} | Description: {command_description}")
                
                # Update previous command
                previous_command = bot_command
            
            # Draw the bounding box around the detected pose
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
        else:
            # If the target is out of the frame
            bot_command = distance_estimator.get_command(0, 0, 0, 0)
            if bot_command != previous_command:
                # Print the command in both bit and text form
                command_bits = bin(bot_command)
                command_description = get_command_description(bot_command)
                print(f"Command as bits: {command_bits} | Description: {command_description}")
                
                # Update previous command
                previous_command = bot_command
        
        # Show the result in a window
        cv2.imshow("Pose Detection with Distance Estimation", img)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture object and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()