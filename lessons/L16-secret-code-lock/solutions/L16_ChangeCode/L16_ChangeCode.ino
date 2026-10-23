// Lesson 16 challenge solution: secret stars, changeable code, lockout
// - The Serial Monitor shows * instead of the digits you type.
// - While the door is open, press A, type a new code, then #.
// - 3 wrong codes in a row lock the keypad for 30 seconds.

#include <Keypad.h>
#include <ESP32Servo.h>

char keys[4][4] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};
byte rowPins[4] = {13, 14, 27, 26};
byte colPins[4] = {25, 4, 16, 17};
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, 4, 4);

const int BUZZER_PIN = 33;
const int RED_PIN = 19;
const int GREEN_PIN = 23;
const int SERVO_PIN = 18;

Servo lock;
String secret = "1234";
String typed = "";
int wrongTries = 0;

// Waits for keys (gives up after timeoutMs with no key). Returns the
// code typed before '#', or "" on timeout or '*'.
String readCode(unsigned long timeoutMs) {
  String code = "";
  unsigned long start = millis();
  while (millis() - start < timeoutMs) {
    char key = keypad.getKey();
    if (!key) continue;
    tone(BUZZER_PIN, 1500, 50);
    start = millis();
    if (key == '#') return code;
    if (key == '*') return "";
    code = code + key;
    Serial.print("*");
  }
  return "";
}

void openLock() {
  Serial.println("\nCorrect! Door open. Press A to change the code.");
  wrongTries = 0;
  digitalWrite(GREEN_PIN, HIGH);
  tone(BUZZER_PIN, 1000, 100);
  delay(150);
  tone(BUZZER_PIN, 2000, 200);
  lock.write(90);

  unsigned long start = millis();
  while (millis() - start < 5000) {
    if (keypad.getKey() == 'A') {
      Serial.println("Type the new code, then #");
      String newCode = readCode(10000);
      if (newCode.length() >= 4) {
        secret = newCode;
        Serial.println("\nNew code saved!");
      } else {
        Serial.println("\nCode must be at least 4 keys. Not changed.");
      }
      break;
    }
  }

  lock.write(0);
  digitalWrite(GREEN_PIN, LOW);
  Serial.println("Locked again.");
}

void wrongCode() {
  wrongTries = wrongTries + 1;
  Serial.println("\nWRONG CODE!");
  digitalWrite(RED_PIN, HIGH);
  tone(BUZZER_PIN, 200, 800);
  delay(1000);
  if (wrongTries >= 3) {
    Serial.println("Too many tries. Keypad locked for 30 seconds.");
    for (int s = 30; s > 0; s--) {
      digitalWrite(RED_PIN, s % 2);
      delay(1000);
    }
    wrongTries = 0;
    Serial.println("You may try again.");
  }
  digitalWrite(RED_PIN, LOW);
}

void setup() {
  Serial.begin(115200);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  lock.attach(SERVO_PIN, 500, 2400);
  lock.write(0);
  Serial.println("Enter the code, then press #");
}

void loop() {
  char key = keypad.getKey();
  if (!key) {
    return;
  }
  tone(BUZZER_PIN, 1500, 50);

  if (key == '*') {
    typed = "";
    Serial.println("\nCleared");
  } else if (key == '#') {
    if (typed == secret) {
      openLock();
    } else {
      wrongCode();
    }
    typed = "";
  } else {
    typed = typed + key;
    Serial.print("*");
  }
}
