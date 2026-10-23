// Lesson 3: Press a button to light an LED
// Button on pin 13 (other leg to GND), yellow LED on 26.

const int BUTTON = 13;
const int LED = 26;

void setup() {
  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(LED, OUTPUT);
}

void loop() {
  if (digitalRead(BUTTON) == LOW) {
    digitalWrite(LED, HIGH);   // pressed
  } else {
    digitalWrite(LED, LOW);    // not pressed
  }
}
