// Lesson 6: Button piano
// Passive buzzer on 33. Five buttons on 13, 14, 16, 17, 18
// (other legs to GND) play C, D, E, F, G.

const int BUZZER = 33;

int keys[] = {13, 14, 16, 17, 18};
int freqs[] = {262, 294, 330, 349, 392};
int lastNote = 0;

void setup() {
  for (int i = 0; i < 5; i++) {
    pinMode(keys[i], INPUT_PULLUP);
  }
}

void loop() {
  int note = 0;
  for (int i = 0; i < 5; i++) {
    if (digitalRead(keys[i]) == LOW) {
      note = freqs[i];
    }
  }

  if (note != lastNote) {
    if (note > 0) {
      tone(BUZZER, note);
    } else {
      noTone(BUZZER);
    }
    lastNote = note;
  }
  delay(10);
}
