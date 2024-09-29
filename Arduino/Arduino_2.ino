// Define motor pins for Motor B (Right Motor, M2)
const int motorB_pwm = 11;   // PWM pin for Motor B
const int motorB_dir1 = 4;   // Direction pin 1 for Motor B
const int motorB_dir2 = 5;   // Direction pin 2 for Motor B

void setup() {
  // Initialize the motor control pins as outputs
  pinMode(motorB_pwm, OUTPUT);
  pinMode(motorB_dir1, OUTPUT);
  pinMode(motorB_dir2, OUTPUT);

  // Start the serial communication to receive commands
  Serial.begin(9600);
  Serial.println("Right Motor Control Ready! Waiting for commands...");
}

void loop() {
  // Check if there is data available on the Serial
  if (Serial.available() > 0) {
    // Read the command from the Serial port
    int command = Serial.parseInt();
    
    // Interpret the command bits and control the motor accordingly
    if (command & 1) {
      // Bit 0 set: Go forward
      Serial.println("Moving right motor FORWARD...");
      digitalWrite(motorB_dir1, HIGH);
      digitalWrite(motorB_dir2, LOW);
      analogWrite(motorB_pwm, 255);  // Set to full speed
    } 
    else if (command & 2) {
      // Bit 1 set: Go backward
      Serial.println("Moving right motor BACKWARD...");
      digitalWrite(motorB_dir1, LOW);
      digitalWrite(motorB_dir2, HIGH);
      analogWrite(motorB_pwm, 255);  // Set to full speed
    } 
    else if (command & 4) {
      // Bit 2 set: Turn left - right motor should go forward
      Serial.println("Turning left (RIGHT MOTOR FORWARD)...");
      digitalWrite(motorB_dir1, HIGH);
      digitalWrite(motorB_dir2, LOW);
      analogWrite(motorB_pwm, 255);  // Set to full speed
    } 
    else if (command & 8) {
      // Bit 3 set: Turn right - right motor should go backward
      Serial.println("Turning right (RIGHT MOTOR BACKWARD)...");
      digitalWrite(motorB_dir1, LOW);
      digitalWrite(motorB_dir2, HIGH);
      analogWrite(motorB_pwm, 255);  // Set to full speed
    } 
    else if (command & 128) {
      // Bit 7 set: Stay
      Serial.println("Stopping right motor...");
      analogWrite(motorB_pwm, 0);  // Stop motor
    }
  }
}