// Lesson 2 challenge solution: light bounces back and forth

int leds[] = {25, 26, 27};
int speed = 150;

void flash(int pin) {
  digitalWrite(pin, HIGH);
  delay(speed);
  digitalWrite(pin, LOW);
}

void setup() {
  for (int i = 0; i < 3; i++) {
    pinMode(leds[i], OUTPUT);
  }
}

void loop() {
  for (int i = 0; i < 3; i++) {
    flash(leds[i]);
  }
  for (int i = 1; i > 0; i--) {
    flash(leds[i]);
  }
}
