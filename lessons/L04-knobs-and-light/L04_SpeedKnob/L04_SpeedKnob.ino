// Lesson 4: The knob sets the blink speed
// Knob on pin 34, yellow LED on pin 26.

const int KNOB = 34;
const int LED = 26;

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
}

void loop() {
  int value = analogRead(KNOB);
  int wait = map(value, 0, 4095, 50, 1000);
  Serial.print("wait:");
  Serial.println(wait);

  digitalWrite(LED, HIGH);
  delay(wait);
  digitalWrite(LED, LOW);
  delay(wait);
}
