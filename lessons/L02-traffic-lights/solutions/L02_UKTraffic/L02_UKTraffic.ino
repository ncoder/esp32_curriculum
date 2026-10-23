// Lesson 2 challenge solution: UK-style traffic light
// Red, then red + yellow together, then green, then yellow.

const int RED = 25;
const int YELLOW = 26;
const int GREEN = 27;

void lights(int r, int y, int g, int wait) {
  digitalWrite(RED, r);
  digitalWrite(YELLOW, y);
  digitalWrite(GREEN, g);
  delay(wait);
}

void setup() {
  pinMode(RED, OUTPUT);
  pinMode(YELLOW, OUTPUT);
  pinMode(GREEN, OUTPUT);
}

void loop() {
  lights(HIGH, LOW, LOW, 3000);    // stop
  lights(HIGH, HIGH, LOW, 1000);   // get ready to go
  lights(LOW, LOW, HIGH, 3000);    // go
  lights(LOW, HIGH, LOW, 1000);    // get ready to stop
}
