// Lesson 8: Light show
// Plays a list of patterns. The knob on pin 34 sets the speed.

const int DATA_PIN = 23;
const int LATCH_PIN = 19;
const int CLOCK_PIN = 18;
const int POT_PIN = 34;

const int NUM_PATTERNS = 8;
const byte patterns[NUM_PATTERNS] = {
  0b10000001,
  0b01000010,
  0b00100100,
  0b00011000,
  0b00011000,
  0b00100100,
  0b01000010,
  0b10000001
};

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
  for (int i = 0; i < NUM_PATTERNS; i++) {
    showByte(patterns[i]);
    int wait = map(analogRead(POT_PIN), 0, 4095, 30, 500);
    delay(wait);
  }
}
