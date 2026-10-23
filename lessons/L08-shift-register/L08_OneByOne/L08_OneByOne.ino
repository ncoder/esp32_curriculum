// Lesson 8: One LED at a time
// 74HC595 shift register: DATA 23, LATCH 19, CLOCK 18.

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
  for (int i = 0; i < 8; i++) {
    showByte(bit(i));
    delay(200);
  }
  for (int i = 0; i < 4; i++) {
    showByte(0b10101010);
    delay(300);
    showByte(0b01010101);
    delay(300);
  }
}
