// Lesson 3 challenge solution: pedestrian crossing
// Traffic light LEDs on 25/26/27, button on 13.
// Cars get green until someone presses the button.

const int RED = 25;
const int YELLOW = 26;
const int GREEN = 27;
const int BUTTON = 13;

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
  pinMode(BUTTON, INPUT_PULLUP);
  lights(LOW, LOW, HIGH, 0);
}

void loop() {
  if (digitalRead(BUTTON) == LOW) {
    delay(1000);                     // wait a moment
    lights(LOW, HIGH, LOW, 2000);    // yellow
    lights(HIGH, LOW, LOW, 5000);    // red: people cross
    lights(LOW, LOW, HIGH, 0);       // green again
  }
}
