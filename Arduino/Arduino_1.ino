// Define motor pins for Motor A (Left Motor, M1)
const int motorA_pwm = 3;    // PWM pin for Motor A
const int motorA_dir1 = 12;  // Direction pin 1 for Motor A
const int motorA_dir2 = 13;  // Direction pin 2 for Motor A

void setup() {
  // Initialize the motor control pins as outputs
  pinMode(motorA_pwm, OUTPUT);
  pinMode(motorA_dir1, OUTPUT);
  pinMode(motorA_dir2, OUTPUT);

  // Start the serial communication to receive commands
  Serial.begin(9600);
  Serial.println("Left Motor Control Ready! Waiting for commands...");
}

void loop() {
  // Check if there is data available on the Serial
  if (Serial.available() > 0) {
    // Read the command from the Serial port
    int command = Serial.parseInt();
    
    // Interpret the command bits and control the motor accordingly
    if (command & 1) {
      // Bit 0 set: Go forward
      Serial.println("Moving left motor FORWARD...");
      digitalWrite(motorA_dir1, HIGH);
      digitalWrite(motorA_dir2, LOW);
      analogWrite(motorA_pwm, 255);  // Set to full speed
    } 
    else if (command & 2) {
      // Bit 1 set: Go backward
      Serial.println("Moving left motor BACKWARD...");
      digitalWrite(motorA_dir1, LOW);
      digitalWrite(motorA_dir2, HIGH);
      analogWrite(motorA_pwm, 255);  // Set to full speed
    } 
    else if (command & 4) {
      // Bit 2 set: Turn left - left motor should go backward
      Serial.println("Turning left (LEFT MOTOR BACKWARD)...");
      digitalWrite(motorA_dir1, LOW);
      digitalWrite(motorA_dir2, HIGH);
      analogWrite(motorA_pwm, 255);  // Set to full speed
    } 
    else if (command & 8) {
      // Bit 3 set: Turn right - left motor should go forward
      Serial.println("Turning right (LEFT MOTOR FORWARD)...");
      digitalWrite(motorA_dir1, HIGH);
      digitalWrite(motorA_dir2, LOW);
      analogWrite(motorA_pwm, 255);  // Set to full speed
    } 
    else if (command & 128) {
      // Bit 7 set: Stay
      Serial.println("Stopping left motor...");
      analogWrite(motorA_pwm, 0);  // Stop motor
    }
  }
}