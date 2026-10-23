// Lesson 13 challenge solution: alarm with an exit delay and a time log
// After arming you get 10 seconds (fast beeps) to leave the room.
// Each alarm prints how long after arming it happened (mm:ss).

const int PIR_PIN = 27;
const int BUTTON_PIN = 13;
const int RED_PIN = 25;
const int GREEN_PIN = 26;
const int BUZZER_PIN = 33;
const int EXIT_DELAY = 10;          // seconds

bool armed = false;
bool wasMoving = false;
int alarms = 0;
unsigned long armedAt = 0;

void showState() {
  digitalWrite(RED_PIN, armed);
  digitalWrite(GREEN_PIN, !armed);
  Serial.println(armed ? "ARMED" : "Disarmed");
}

void exitCountdown() {
  for (int s = EXIT_DELAY; s > 0; s--) {
    Serial.print("Leave the room! ");
    Serial.println(s);
    tone(BUZZER_PIN, 2000, 80);
    delay(1000);
    if (digitalRead(BUTTON_PIN) == LOW) {   // pressed again: cancel
      armed = false;
      while (digitalRead(BUTTON_PIN) == LOW) {
        delay(10);
      }
      return;
    }
  }
}

void printTime(unsigned long ms) {
  int seconds = ms / 1000;
  int minutes = seconds / 60;
  seconds = seconds % 60;
  if (minutes < 10) Serial.print("0");
  Serial.print(minutes);
  Serial.print(":");
  if (seconds < 10) Serial.print("0");
  Serial.println(seconds);
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
    while (digitalRead(BUTTON_PIN) == LOW) {
      delay(10);
    }
    if (armed) {
      exitCountdown();
      armedAt = millis();
    }
    showState();
    wasMoving = digitalRead(PIR_PIN) == HIGH;
  }

  bool moving = digitalRead(PIR_PIN) == HIGH;
  if (armed && moving && !wasMoving) {
    alarms = alarms + 1;
    Serial.print("Alarm ");
    Serial.print(alarms);
    Serial.print(" at ");
    printTime(millis() - armedAt);
    siren();
  }
  wasMoving = moving;
  delay(20);
}
