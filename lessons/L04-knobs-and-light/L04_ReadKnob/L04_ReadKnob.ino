// Lesson 4: Read the knob
// Potentiometer: outer legs to 3V3 and GND, middle leg to pin 34.

const int KNOB = 34;

void setup() {
  Serial.begin(115200);
}

void loop() {
  int value = analogRead(KNOB);
  Serial.print("knob:");
  Serial.println(value);
  delay(50);
}
