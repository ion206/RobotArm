#include <Servo.h>

// ----- PWM bounds for each servo -----!!
// Adjust these values to match your servo's calibration for 0° and 180°.
const int SERVO1_MIN_PULSE = 1230;   // default minimum pulse width in microseconds
const int SERVO1_MAX_PULSE = 2400;  // default maximum pulse width in microseconds

const int SERVO2_MIN_PULSE = 900;
const int SERVO2_MAX_PULSE = 2066;

const int SERVO3_MIN_PULSE = 200;
const int SERVO3_MAX_PULSE = 350;

const int SERVO4_MIN_PULSE = 550;
const int SERVO4_MAX_PULSE = 2050;

// ----- Servo pins -----
const int SERVO1_PIN = 6;
const int SERVO2_PIN = 5;
const int SERVO3_PIN = 10;
const int SERVO4_PIN = 11;

// Create servo objects
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

void setup() {
  // Attach servos with the specified PWM bounds
  servo1.attach(SERVO1_PIN, SERVO1_MIN_PULSE, SERVO1_MAX_PULSE);
  servo2.attach(SERVO2_PIN, SERVO2_MIN_PULSE, SERVO2_MAX_PULSE);
  servo3.attach(SERVO3_PIN, SERVO3_MIN_PULSE, SERVO3_MAX_PULSE);
  servo4.attach(SERVO4_PIN, SERVO4_MIN_PULSE, SERVO4_MAX_PULSE);
  
  // Start serial communication
  Serial.begin(9600);
  Serial.println("Enter 4 angles (0-180) separated by any delimiter:");
}

void loop() {
  // Check if data is available on Serial
  if (Serial.available() > 0) {
    // Read 4 integers from the serial stream using parseInt (it skips non-digit characters)
    int angle1 = Serial.parseInt();
    int angle2 = Serial.parseInt();
    int angle3 = Serial.parseInt();
    int angle4 = Serial.parseInt();
    
    // Validate that each angle is within 0-180
    if (
        angle2 < 0 || angle2 > 180 ||
        angle3 < 0 || angle3 > 180){
      Serial.println("Invalid input. Angles must be between 0 and 180.");
    } else {
      angle1 = SERVO1_MIN_PULSE + (angle1 * ((SERVO1_MAX_PULSE - SERVO1_MIN_PULSE)/180));
      // Set servos to the specified angles
      servo1.writeMicroseconds(angle1);
      servo2.write(angle2);
      servo3.write(angle3);
      servo4.write(angle4);
      
      Serial.print("Servo 1 set to: ");
      Serial.println(angle1);
      Serial.print("Servo 2 set to: ");
      Serial.println(angle2);
      Serial.print("Servo 3 set to: ");
      Serial.println(angle3);
      Serial.print("Servo 4 set to: ");
      Serial.println(angle4);
    }
    
    // Clear any remaining input until newline (if any)
    while (Serial.available() > 0) {
      char c = Serial.read();
      if(c == '\n') break;
    }
    
    // Prompt for next input
    Serial.println("\nEnter 4 angles (0-180) separated by any delimiter:");
    Serial.println(servo4.readMicroseconds());
  }
}
