// Appendix A: test a push button
// Button on pin 13, other leg to GND. Open the Serial Monitor.

const int BUTTON = 13;

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON, INPUT_PULLUP);   // reads HIGH until you press
}

void loop() {
  if (digitalRead(BUTTON) == LOW) {
    Serial.println("pressed");
  } else {
    Serial.println("-");
  }
  delay(200);
}
