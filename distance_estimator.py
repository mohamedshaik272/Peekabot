import cv2

class DistanceEstimator:
    def __init__(self, frame_width, frame_height, ideal_distance=2.5):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.ideal_distance = ideal_distance
        self.ideal_box_height = int(frame_height * 0.6)  # Assuming ideal height is 60% of frame height
        self.center_x = frame_width // 2
        self.center_y = frame_height // 2
        self.horizontal_threshold = frame_width // 4  # Increased to make center area smaller
        self.vertical_threshold = frame_height // 4  # For drawing purposes only

    def estimate_distance(self, box_height):
        # Estimate distance based on box height
        return self.ideal_distance * (self.ideal_box_height / box_height)

    def get_command(self, x_min, y_min, x_max, y_max):
        if x_min == 0 and y_min == 0 and x_max == 0 and y_max == 0:
            return "ALERT: TARGET OUT OF FRAME!!!!!!"

        box_center_x = (x_min + x_max) // 2
        box_height = y_max - y_min

        distance = self.estimate_distance(box_height)

        commands = []

        # Check distance first
        if distance < self.ideal_distance * 0.8:
            commands.append("GO BACK")
        elif distance > self.ideal_distance * 1.2:
            commands.append("GO FORWARD")

        # Check horizontal position
        if box_center_x < self.center_x - self.horizontal_threshold:
            commands.append("TURN LEFT")
        elif box_center_x > self.center_x + self.horizontal_threshold:
            commands.append("TURN RIGHT")

        # If no movement command is added, BOT should stay
        if not commands:
            commands.append("STAY")

        return " and ".join(commands)

    def draw_guide(self, img):
        # Draw center crosshair
        cv2.line(img, (self.center_x, 0), (self.center_x, self.frame_height), (0, 255, 0), 1)
        cv2.line(img, (0, self.center_y), (self.frame_width, self.center_y), (0, 255, 0), 1)

        # Draw threshold lines
        cv2.line(img, (self.center_x - self.horizontal_threshold, 0),
                 (self.center_x - self.horizontal_threshold, self.frame_height), (0, 255, 0), 1)
        cv2.line(img, (self.center_x + self.horizontal_threshold, 0),
                 (self.center_x + self.horizontal_threshold, self.frame_height), (0, 255, 0), 1)
        cv2.line(img, (0, self.center_y - self.vertical_threshold),
                 (self.frame_width, self.center_y - self.vertical_threshold), (0, 255, 0), 1)
        cv2.line(img, (0, self.center_y + self.vertical_threshold),
                 (self.frame_width, self.center_y + self.vertical_threshold), (0, 255, 0), 1)

        return img