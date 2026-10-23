// Lesson 6 challenge solution: police siren
// Passive buzzer on 33. The pitch sweeps up and down.

const int BUZZER = 33;

void setup() {
}

void loop() {
  for (int f = 500; f <= 1200; f = f + 10) {
    tone(BUZZER, f);
    delay(5);
  }
  for (int f = 1200; f >= 500; f = f - 10) {
    tone(BUZZER, f);
    delay(5);
  }
}
