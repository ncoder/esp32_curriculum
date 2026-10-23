// Lesson 12 challenge solution: hand theremin
// Move your hand closer for a higher note. Nothing in range = silence.

const int TRIG_PIN = 17;
const int ECHO_PIN = 16;
const int BUZZER_PIN = 33;

float readDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long echoTime = pulseIn(ECHO_PIN, HIGH, 30000);
  if (echoTime == 0) {
    return -1;
  }
  return echoTime * 0.0343 / 2;
}

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  float cm = readDistance();
  if (cm < 3 || cm > 40) {
    noTone(BUZZER_PIN);
  } else {
    int note = map((int)cm, 3, 40, 1500, 200);
    tone(BUZZER_PIN, note);
  }
  delay(50);
}
