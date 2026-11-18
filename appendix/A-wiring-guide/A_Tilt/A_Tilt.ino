// Appendix A: test the tilt switch
// Tilt switch on pin 14, other leg to GND. Open the Serial Monitor.

const int TILT = 14;

void setup() {
  Serial.begin(115200);
  pinMode(TILT, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(TILT) == LOW) {
    Serial.println("upright (ball touching the legs)");
  } else {
    Serial.println("tipped over");
  }
  delay(200);
}
