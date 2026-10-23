// Lesson 13: Burglar alarm
// Button on 13 arms/disarms. Red LED 25, green LED 26, buzzer 33.

const int PIR_PIN = 27;
const int BUTTON_PIN = 13;
const int RED_PIN = 25;
const int GREEN_PIN = 26;
const int BUZZER_PIN = 33;

bool armed = false;
bool wasMoving = false;
int alarms = 0;

void showState() {
  digitalWrite(RED_PIN, armed);
  digitalWrite(GREEN_PIN, !armed);
  if (armed) {
    Serial.println("ARMED");
  } else {
    Serial.println("Disarmed");
  }
}

void siren() {
  for (int i = 0; i < 6; i++) {
    digitalWrite(RED_PIN, HIGH);
    tone(BUZZER_PIN, 1200);
    delay(250);
    digitalWrite(RED_PIN, LOW);
    tone(BUZZER_PIN, 800);
    delay(250);
  }
  noTone(BUZZER_PIN);
  showState();
}

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  showState();
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    armed = !armed;
    showState();
    tone(BUZZER_PIN, 2000, 100);
    while (digitalRead(BUTTON_PIN) == LOW) {
      delay(10);                    // wait for the finger to lift
    }
  }

  bool moving = digitalRead(PIR_PIN) == HIGH;
  if (armed && moving && !wasMoving) {
    alarms = alarms + 1;
    Serial.print("INTRUDER! Alarm number ");
    Serial.println(alarms);
    siren();
  }
  wasMoving = moving;
  delay(20);
}
