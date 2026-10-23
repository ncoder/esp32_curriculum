// Lesson 4 challenge solution: knob level meter
// Knob on 34; LEDs green 27, yellow 26, red 25 light up in turn.

const int KNOB = 34;
const int GREEN = 27;
const int YELLOW = 26;
const int RED = 25;

void setup() {
  pinMode(GREEN, OUTPUT);
  pinMode(YELLOW, OUTPUT);
  pinMode(RED, OUTPUT);
}

void loop() {
  int level = analogRead(KNOB) / 1024;   // 0, 1, 2 or 3

  digitalWrite(GREEN, level >= 1);
  digitalWrite(YELLOW, level >= 2);
  digitalWrite(RED, level >= 3);
  delay(50);
}
