import cv2
import mediapipe as mp

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

                # Update the min/max coordinates to include the head and body landmarks
                if x < x_min:
                    x_min = x
                if y < y_min:
                    y_min = y
                if x > x_max:
                    x_max = x
                if y > y_max:
                    y_max = y

            # Add some padding to the bounding box (optional, to ensure head is fully inside the box)
            padding = 20  # Add some padding to make the box larger
            x_min = max(0, x_min - padding)
            y_min = max(0, y_min - padding)
            x_max = min(frameWidth, x_max + padding)
            y_max = min(frameHeight, y_max + padding)

            if y <= 750:
                print("BOT COMMAND: GO FORWARD!")
            print(f"X: {x}")
            print(f"Y: {y}\n")

            # Draw the bounding box around the detected pose including the head
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
        else:
            print("ALERT: TARGET OUT OF FRAME!!!!!!")

        # Show the result in a window
        cv2.imshow("Pose Detection with Bounding Box Including Head", img)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture object and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()