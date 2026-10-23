// Lesson 3: Count button presses
// Count button on 13, reset button on 14 (both to GND).

const int COUNT_BTN = 13;
const int RESET_BTN = 14;

int count = 0;
bool wasPressed = false;

void setup() {
  Serial.begin(115200);
  pinMode(COUNT_BTN, INPUT_PULLUP);
  pinMode(RESET_BTN, INPUT_PULLUP);
}

void loop() {
  bool pressed = digitalRead(COUNT_BTN) == LOW;

  if (pressed && !wasPressed) {
    count = count + 1;
    Serial.print("Presses: ");
    Serial.println(count);
  }
  wasPressed = pressed;

  if (digitalRead(RESET_BTN) == LOW) {
    count = 0;
    Serial.println("Reset to 0!");
    delay(300);
  }

  delay(20);
}
