// Lesson 3: Press once for on, press again for off
// Same wiring as L03_Button.

const int BUTTON = 13;
const int LED = 26;

bool ledOn = false;
bool wasPressed = false;

void setup() {
  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(LED, OUTPUT);
}

void loop() {
  bool pressed = digitalRead(BUTTON) == LOW;

  if (pressed && !wasPressed) {
    ledOn = !ledOn;
    digitalWrite(LED, ledOn);
  }

  wasPressed = pressed;
  delay(20);   // ignore the bouncing contacts
}
