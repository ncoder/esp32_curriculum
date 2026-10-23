// Lesson 6 challenge solution: piano with coloured lights
// Passive buzzer on 33, buttons on 13, 14, 16, 17, 18,
// RGB LED on 25/26/27 (from Lesson 5).

const int BUZZER = 33;
const int RED = 25;
const int GREEN = 26;
const int BLUE = 27;

int keys[] = {13, 14, 16, 17, 18};
int freqs[] = {262, 294, 330, 349, 392};
int colors[5][3] = {
  {255, 0, 0}, {255, 128, 0}, {0, 255, 0}, {0, 0, 255}, {128, 0, 255}
};
int lastKey = -1;

void setColor(int r, int g, int b) {
  analogWrite(RED, r);
  analogWrite(GREEN, g);
  analogWrite(BLUE, b);
}

void setup() {
  for (int i = 0; i < 5; i++) {
    pinMode(keys[i], INPUT_PULLUP);
  }
}

void loop() {
  int key = -1;
  for (int i = 0; i < 5; i++) {
    if (digitalRead(keys[i]) == LOW) {
      key = i;
    }
  }

  if (key != lastKey) {
    if (key >= 0) {
      tone(BUZZER, freqs[key]);
      setColor(colors[key][0], colors[key][1], colors[key][2]);
    } else {
      noTone(BUZZER);
      setColor(0, 0, 0);
    }
    lastKey = key;
  }
  delay(10);
}
