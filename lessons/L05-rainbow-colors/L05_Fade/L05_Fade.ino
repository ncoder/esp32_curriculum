// Lesson 5: Fade an LED in and out
// Yellow LED on pin 26 (from Lesson 2).

const int LED = 26;

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  for (int brightness = 0; brightness <= 255; brightness++) {
    analogWrite(LED, brightness);
    delay(5);
  }
  for (int brightness = 255; brightness >= 0; brightness--) {
    analogWrite(LED, brightness);
    delay(5);
  }
}
