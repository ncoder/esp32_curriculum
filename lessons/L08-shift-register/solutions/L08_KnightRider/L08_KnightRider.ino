// Lesson 8 challenge solution: Knight Rider scanner
// One light (with a dim-looking tail of two) sweeps left and right.

const int DATA_PIN = 23;
const int LATCH_PIN = 19;
const int CLOCK_PIN = 18;

void showByte(byte leds) {
  digitalWrite(LATCH_PIN, LOW);
  shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, leds);
  digitalWrite(LATCH_PIN, HIGH);
}

void setup() {
  pinMode(DATA_PIN, OUTPUT);
  pinMode(LATCH_PIN, OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);
}

void loop() {
  for (int i = 0; i < 7; i++) {      // move left
    showByte(bit(i) | bit(i + 1));
    delay(80);
  }
  for (int i = 7; i > 0; i--) {      // move right
    showByte(bit(i) | bit(i - 1));
    delay(80);
  }
}
