// Lesson 7: Test every segment
// Lights segments a, b, c, d, e, f, g and dp one at a time.

const int segPins[8] = {23, 22, 21, 19, 18, 17, 16, 4};
const String names[8] = {"a", "b", "c", "d", "e", "f", "g", "dp"};

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < 8; i++) {
    pinMode(segPins[i], OUTPUT);
  }
}

void loop() {
  for (int i = 0; i < 8; i++) {
    Serial.println(names[i]);
    digitalWrite(segPins[i], HIGH);
    delay(500);
    digitalWrite(segPins[i], LOW);
  }
}
