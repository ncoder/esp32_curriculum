// Lesson 12: Parking sensor
// Beeps faster as you get closer. Passive buzzer on pin 33.

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
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  float cm = readDistance();
  Serial.println(cm);

  if (cm < 0 || cm > 50) {
    noTone(BUZZER_PIN);           // far away: stay quiet
    delay(200);
  } else if (cm < 5) {
    tone(BUZZER_PIN, 1000);       // very close: non-stop beep
    delay(100);
  } else {
    tone(BUZZER_PIN, 1000, 60);   // short beep...
    delay(cm * 10);               // ...gap gets shorter when close
  }
}
