// Lesson 8 challenge solution: bar graph meter
// Turn the knob on pin 34: more LEDs light up the further you turn it.

const int DATA_PIN = 23;
const int LATCH_PIN = 19;
const int CLOCK_PIN = 18;
const int POT_PIN = 34;

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
  int level = map(analogRead(POT_PIN), 0, 4095, 0, 8);
  byte leds = 0;
  for (int i = 0; i < level; i++) {
    leds = leds + bit(i);
  }
  showByte(leds);
  Serial.println(level);
  delay(50);
}
