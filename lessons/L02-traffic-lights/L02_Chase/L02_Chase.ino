// Lesson 2: Light chase
// Same wiring. A light runs along the LEDs.

int leds[] = {25, 26, 27};
int speed = 150;

void setup() {
  for (int i = 0; i < 3; i++) {
    pinMode(leds[i], OUTPUT);
  }
}

void loop() {
  for (int i = 0; i < 3; i++) {
    digitalWrite(leds[i], HIGH);
    delay(speed);
    digitalWrite(leds[i], LOW);
  }
}
