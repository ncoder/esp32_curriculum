// Lesson 3: Shake alarm
// Tilt switch on pin 14 (other leg to GND), red LED on 25.

const int TILT = 14;
const int ALARM_LED = 25;

int lastTilt;
int shakes = 0;

void setup() {
  Serial.begin(115200);
  pinMode(TILT, INPUT_PULLUP);
  pinMode(ALARM_LED, OUTPUT);
  lastTilt = digitalRead(TILT);
}

void loop() {
  int tilt = digitalRead(TILT);

  if (tilt != lastTilt) {
    shakes = shakes + 1;
    Serial.print("Shake detected! Total: ");
    Serial.println(shakes);

    digitalWrite(ALARM_LED, HIGH);
    delay(1000);
    digitalWrite(ALARM_LED, LOW);

    lastTilt = digitalRead(TILT);
  }
}
