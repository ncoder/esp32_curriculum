// Lesson 7 challenge solution: dice with clicking sound and a spin
// Passive buzzer on pin 33. The outer segments spin while rolling.

const int BUTTON_PIN = 13;
const int BUZZER_PIN = 33;
const int segPins[7] = {23, 22, 21, 19, 18, 17, 16};

const int digits[10][7] = {
// a  b  c  d  e  f  g
  {1, 1, 1, 1, 1, 1, 0},  // 0
  {0, 1, 1, 0, 0, 0, 0},  // 1
  {1, 1, 0, 1, 1, 0, 1},  // 2
  {1, 1, 1, 1, 0, 0, 1},  // 3
  {0, 1, 1, 0, 0, 1, 1},  // 4
  {1, 0, 1, 1, 0, 1, 1},  // 5
  {1, 0, 1, 1, 1, 1, 1},  // 6
  {1, 1, 1, 0, 0, 0, 0},  // 7
  {1, 1, 1, 1, 1, 1, 1},  // 8
  {1, 1, 1, 1, 0, 1, 1}   // 9
};

void showDigit(int n) {
  for (int s = 0; s < 7; s++) {
    digitalWrite(segPins[s], digits[n][s]);
  }
}

void showOneSegment(int seg) {
  for (int s = 0; s < 7; s++) {
    digitalWrite(segPins[s], s == seg);
  }
}

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  for (int s = 0; s < 7; s++) {
    pinMode(segPins[s], OUTPUT);
  }
  showDigit(0);
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    for (int i = 0; i < 18; i++) {
      showOneSegment(i % 6);  // segments a to f go round the edge
      tone(BUZZER_PIN, 1500, 10);
      delay(30 + i * 8);
    }
    int roll = random(1, 7);
    showDigit(roll);
    tone(BUZZER_PIN, 880, 200);
    while (digitalRead(BUTTON_PIN) == LOW) {
      delay(10);
    }
  }
}
