// Lesson 14 challenge solution: robot arm with memory
// Steer with the joystick and click to save up to 5 positions.
// After the 5th click the servo plays the moves back 3 times.

#include <ESP32Servo.h>

const int SERVO_PIN = 18;
const int X_PIN = 34;
const int SW_PIN = 14;
const int MAX_MOVES = 5;

Servo myServo;
int angle = 90;
int moves[MAX_MOVES];
int saved = 0;

void playBack() {
  for (int round = 0; round < 3; round++) {
    for (int i = 0; i < MAX_MOVES; i++) {
      Serial.print("Move ");
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.println(moves[i]);
      myServo.write(moves[i]);
      delay(700);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(SW_PIN, INPUT_PULLUP);
  myServo.attach(SERVO_PIN, 500, 2400);
  myServo.write(angle);
  Serial.println("Steer, then click to save a position.");
}

void loop() {
  int x = analogRead(X_PIN);
  if (x < 1000) {
    angle = angle + 2;
  } else if (x > 3000) {
    angle = angle - 2;
  }
  angle = constrain(angle, 0, 180);
  myServo.write(angle);

  if (digitalRead(SW_PIN) == LOW) {
    moves[saved] = angle;
    saved = saved + 1;
    Serial.print("Saved position ");
    Serial.println(saved);
    while (digitalRead(SW_PIN) == LOW) {
      delay(10);
    }
    if (saved == MAX_MOVES) {
      playBack();
      saved = 0;
      Serial.println("Ready for new moves!");
    }
  }
  delay(20);
}
