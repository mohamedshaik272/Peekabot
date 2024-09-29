import cv2

class DistanceEstimator:
    def __init__(self, frame_width, frame_height, ideal_distance=2.5):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.ideal_distance = ideal_distance
        self.ideal_box_height = int(frame_height * 0.6)  # Assuming ideal height is 60% of frame height
        self.center_x = frame_width // 2
        self.center_y = frame_height // 2
        self.horizontal_threshold = frame_width // 4  # Threshold for horizontal movement

    def estimate_distance(self, box_height):
        # Estimate distance based on box height
        return self.ideal_distance * (self.ideal_box_height / box_height)

    def get_command(self, x_min, y_min, x_max, y_max):
        command = 0  # Initialize the command as 0

        if x_min == 0 and y_min == 0 and x_max == 0 and y_max == 0:
            # Target out of frame
            command |= 16  # Set bit 4 (target out of range)
            return command

        box_center_x = (x_min + x_max) // 2
        box_height = y_max - y_min

        # Estimate the distance to determine if we should move forward or backward
        distance = self.estimate_distance(box_height)

        # Set the bits for distance-based commands
        if distance < self.ideal_distance * 0.8:
            command |= 2  # Set bit 1 (go back)
        elif distance > self.ideal_distance * 1.2:
            command |= 1  # Set bit 0 (go forward)

        # Set the bits for horizontal position-based commands
        if box_center_x < self.center_x - self.horizontal_threshold:
            if command & 1:  # If go forward bit is already set
                command |= 4  # Set bit 2 (turn left) to indicate forward and left
            else:
                command |= 4  # Set bit 2 (turn left)
        elif box_center_x > self.center_x + self.horizontal_threshold:
            if command & 1:  # If go forward bit is already set
                command |= 8  # Set bit 3 (turn right) to indicate forward and right
            else:
                command |= 8  # Set bit 3 (turn right)

        # If no movement command is added, bot should stay
        if command == 0:
            command |= 128  # Set bit 7 (stay)

        return command

    def draw_guide(self, img):
        # Draw center crosshair
        cv2.line(img, (self.center_x, 0), (self.center_x, self.frame_height), (0, 255, 0), 1)
        cv2.line(img, (0, self.center_y), (self.frame_width, self.center_y), (0, 255, 0), 1)

        # Draw horizontal threshold lines
        cv2.line(img, (self.center_x - self.horizontal_threshold, 0),
                 (self.center_x - self.horizontal_threshold, self.frame_height), (0, 255, 0), 1)
        cv2.line(img, (self.center_x + self.horizontal_threshold, 0),
                 (self.center_x + self.horizontal_threshold, self.frame_height), (0, 255, 0), 1)

        return img