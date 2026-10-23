// Lesson 12: Measure distance with sound
// HC-SR04: TRIG on pin 17, ECHO on pin 16 (through the divider).

const int TRIG_PIN = 17;
const int ECHO_PIN = 16;

float readDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);   // a 10 microsecond "ping"
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long echoTime = pulseIn(ECHO_PIN, HIGH, 30000);
  if (echoTime == 0) {
    return -1;                    // no echo came back
  }
  return echoTime * 0.0343 / 2;
}

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  float cm = readDistance();
  if (cm < 0) {
    Serial.println("Nothing in range");
  } else {
    Serial.print("Distance: ");
    Serial.print(cm);
    Serial.println(" cm");
  }
  delay(200);
}
