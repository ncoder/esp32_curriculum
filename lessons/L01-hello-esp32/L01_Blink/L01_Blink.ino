// Lesson 1: Blink an LED
// LED + 220 ohm resistor on pin 26.

const int LED_PIN = 26;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);  // LED on
  delay(500);
  digitalWrite(LED_PIN, LOW);   // LED off
  delay(500);
}
