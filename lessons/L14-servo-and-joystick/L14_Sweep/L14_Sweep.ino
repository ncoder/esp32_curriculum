// Lesson 14: Servo sweep
// Servo signal (orange wire) on pin 18.

#include <ESP32Servo.h>

const int SERVO_PIN = 18;
Servo myServo;

void setup() {
  myServo.attach(SERVO_PIN, 500, 2400);
}

void loop() {
  for (int angle = 0; angle <= 180; angle++) {
    myServo.write(angle);
    delay(15);
  }
  for (int angle = 180; angle >= 0; angle--) {
    myServo.write(angle);
    delay(15);
  }
}
