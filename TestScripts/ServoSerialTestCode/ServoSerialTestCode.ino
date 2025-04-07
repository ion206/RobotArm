#include <Servo.h>

// ----- PWM bounds for each servo -----
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

  int values[5];  // Array to store five integers


void setup() {
  // Attach servos with the specified PWM bounds
  servo1.attach(SERVO1_PIN, SERVO1_MIN_PULSE, SERVO1_MAX_PULSE);
  servo2.attach(SERVO2_PIN, SERVO2_MIN_PULSE, SERVO2_MAX_PULSE);
  servo3.attach(SERVO3_PIN, SERVO3_MIN_PULSE, SERVO3_MAX_PULSE);
  servo4.attach(SERVO4_PIN, SERVO4_MIN_PULSE, SERVO4_MAX_PULSE);
  
  // Start serial communication
  Serial.begin(115200);
  while (!Serial) {
    ; // Wait for serial port to connect (needed for some boards)
  }
}

void loop() {
 if (Serial.available() > 0) {
    // Read an entire line ending with '\n'
    String input = Serial.readStringUntil('\n');
    
    // Temporary variables for five integers
    int a, b, c, d, e;
    // Use sscanf to parse the integers from the string
    if (sscanf(input.c_str(), "%d %d %d %d %d", &a, &b, &c, &d, &e) == 5) {
        values[0] = a;
        values[1] = b;
        values[2] = c;
        values[3] = d;
        values[4] = e;

    // Echo the received integers back over serial (space-separated)
    for (int i = 0; i < 5; i++) {
      Serial.print(values[i]);
      if (i < 4) {
        Serial.print(" ");
      }
    }
    Serial.println(); // End the message with a newline
  }}
    
      //values[0] = SERVO1_MIN_PULSE + (values[0] * ((SERVO1_MAX_PULSE - SERVO1_MIN_PULSE)/180));
      // Set servos to the specified angles
      servo1.write(values[0]);
      servo2.write(values[1]);
      servo3.write(values[2]);
      servo4.write(values[3]);
      /*
      Serial.print("Servo 1 set to: ");
      Serial.println(values[0]);
      Serial.print("Servo 2 set to: ");
      Serial.println(values[1]);
      Serial.print("Servo 3 set to: ");
      Serial.println(values[2]);
      Serial.print("Servo 4 set to: ");
      Serial.println(values[3]);
      */
    }

