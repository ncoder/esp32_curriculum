// Lesson 8: Count in binary
// The 8 LEDs show the number in binary. Watch the Serial Monitor too!

const int DATA_PIN = 23;
const int LATCH_PIN = 19;
const int CLOCK_PIN = 18;

void showByte(byte leds) {
  digitalWrite(LATCH_PIN, LOW);
  shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, leds);
  digitalWrite(LATCH_PIN, HIGH);
}

void setup() {
  Serial.begin(115200);
  pinMode(DATA_PIN, OUTPUT);
  pinMode(LATCH_PIN, OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);
}

void loop() {
  for (int n = 0; n < 256; n++) {
    showByte(n);
    Serial.print(n);
    Serial.print(" in binary is ");
    Serial.println(n, BIN);
    delay(500);
  }
}
