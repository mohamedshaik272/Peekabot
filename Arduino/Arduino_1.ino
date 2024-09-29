// Define motor pins for Motor A (Front Motor, M1)
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
  Serial.println("Front Motor Control Ready! Waiting for commands...");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();  // Remove extra whitespace or newline characters

    if (command == "FORWARD") {
      Serial.println("Moving front motor FORWARD...");
      digitalWrite(motorA_dir1, HIGH);
      digitalWrite(motorA_dir2, LOW);
      analogWrite(motorA_pwm, 255);  // Full speed
    } else if (command == "BACKWARD") {
      Serial.println("Moving front motor BACKWARD...");
      digitalWrite(motorA_dir1, LOW);
      digitalWrite(motorA_dir2, HIGH);
      analogWrite(motorA_pwm, 255);  // Full speed
    } else if (command == "STOP") {
      Serial.println("Stopping front motor...");
      analogWrite(motorA_pwm, 0);
    }
  }
}