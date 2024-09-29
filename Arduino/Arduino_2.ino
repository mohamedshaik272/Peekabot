// Define motor pins for Motor B (Back Motor, M2)
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
  Serial.println("Back Motor Control Ready! Waiting for commands...");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();  // Remove extra whitespace or newline characters

    if (command == "FORWARD") {
      Serial.println("Moving back motor FORWARD...");
      digitalWrite(motorB_dir1, HIGH);
      digitalWrite(motorB_dir2, LOW);
      analogWrite(motorB_pwm, 255);  // Full speed
    } else if (command == "BACKWARD") {
      Serial.println("Moving back motor BACKWARD...");
      digitalWrite(motorB_dir1, LOW);
      digitalWrite(motorB_dir2, HIGH);
      analogWrite(motorB_pwm, 255);  // Full speed
    } else if (command == "STOP") {
      Serial.println("Stopping back motor...");
      analogWrite(motorB_pwm, 0);
    }
  }
}
