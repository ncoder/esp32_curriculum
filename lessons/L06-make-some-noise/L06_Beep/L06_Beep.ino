// Lesson 6: Beep with the active buzzer
// Active buzzer: + leg to pin 33, other leg to GND.

const int BUZZER = 33;

void beep(int length) {
  digitalWrite(BUZZER, HIGH);
  delay(length);
  digitalWrite(BUZZER, LOW);
  delay(150);
}

void setup() {
  pinMode(BUZZER, OUTPUT);
}

void loop() {
  beep(100);
  beep(100);
  beep(400);
  delay(2000);
}
