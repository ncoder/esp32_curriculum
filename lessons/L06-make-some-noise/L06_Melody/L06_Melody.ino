// Lesson 6: Play a tune on the passive buzzer
// Passive buzzer: + leg to pin 33, other leg to GND.

const int BUZZER = 33;
const int TEMPO = 300;

int notes[] = {262, 262, 392, 392, 440, 440, 392,
               349, 349, 330, 330, 294, 294, 262};
int beats[] = {1, 1, 1, 1, 1, 1, 2,
               1, 1, 1, 1, 1, 1, 2};

void setup() {
}

void loop() {
  for (int i = 0; i < 14; i++) {
    tone(BUZZER, notes[i]);
    delay(beats[i] * TEMPO);
    noTone(BUZZER);
    delay(50);
  }
  delay(2000);
}
