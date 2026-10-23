// Lesson 14: Joystick-controlled servo
// Push the stick left/right to turn. Click to go back to the middle.

#include <ESP32Servo.h>

const int SERVO_PIN = 18;
const int X_PIN = 34;
const int SW_PIN = 14;

Servo myServo;
int angle = 90;

void setup() {
  Serial.begin(115200);
  pinMode(SW_PIN, INPUT_PULLUP);
  myServo.attach(SERVO_PIN, 500, 2400);
  myServo.write(angle);
}

void loop() {
  int x = analogRead(X_PIN);

  if (x < 1000) {
    angle = angle + 2;              // stick pushed one way
  } else if (x > 3000) {
    angle = angle - 2;              // stick pushed the other way
  }
  if (digitalRead(SW_PIN) == LOW) {
    angle = 90;
  }

  angle = constrain(angle, 0, 180);
  myServo.write(angle);
  Serial.println(angle);
  delay(20);
}
