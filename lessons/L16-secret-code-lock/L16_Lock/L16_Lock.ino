// Lesson 16: Secret code lock
// Type the code then #. Press * to start again.

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

void openLock() {
  Serial.println("Correct! Door open.");
  digitalWrite(GREEN_PIN, HIGH);
  lock.write(90);
  delay(5000);
  lock.write(0);
  digitalWrite(GREEN_PIN, LOW);
}

void wrongCode() {
  Serial.println("WRONG CODE!");
  digitalWrite(RED_PIN, HIGH);
  tone(BUZZER_PIN, 200, 800);
  delay(1000);
  digitalWrite(RED_PIN, LOW);
}

void setup() {
  Serial.begin(115200);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  lock.attach(SERVO_PIN, 500, 2400);
  lock.write(0);
}

void loop() {
  char key = keypad.getKey();
  if (!key) {
    return;                         // no key pressed: try again
  }
  tone(BUZZER_PIN, 1500, 50);
  if (key == '*') {
    typed = "";
    Serial.println("Cleared");
  } else if (key == '#') {
    if (typed == secret) {
      openLock();
    } else {
      wrongCode();
    }
    typed = "";
  } else {
    typed = typed + key;
    Serial.println(typed);
  }
}
