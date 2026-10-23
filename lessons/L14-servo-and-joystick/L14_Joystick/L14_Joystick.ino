// Lesson 14: Read the joystick
// VRx on 34, VRy on 35, SW (button) on 14.

const int X_PIN = 34;
const int Y_PIN = 35;
const int SW_PIN = 14;

void setup() {
  Serial.begin(115200);
  pinMode(SW_PIN, INPUT_PULLUP);
}

void loop() {
  int x = analogRead(X_PIN);
  int y = analogRead(Y_PIN);
  bool pressed = digitalRead(SW_PIN) == LOW;

  Serial.print("X: ");
  Serial.print(x);
  Serial.print("  Y: ");
  Serial.print(y);
  if (pressed) {
    Serial.print("  CLICK!");
  }
  Serial.println();
  delay(100);
}
