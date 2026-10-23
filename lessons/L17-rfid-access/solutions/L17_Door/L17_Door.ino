// Lesson 17 challenge solution: RFID door with a servo lock
// Allowed card opens the "door" (servo on 13) for 3 seconds.
// Also counts failed attempts and sounds an alarm after 3.

#include <SPI.h>
#include <MFRC522.h>
#include <ESP32Servo.h>

const int SS_PIN = 5;
const int RST_PIN = 4;
const int RED_PIN = 25;
const int GREEN_PIN = 27;
const int BUZZER_PIN = 33;
const int SERVO_PIN = 13;   // 18 is busy: it's the SPI clock

String allowed[] = {"A3 4F 12 9B", "04 7E 2C 1A"};
const int NUM_ALLOWED = 2;

MFRC522 rfid(SS_PIN, RST_PIN);
Servo door;
int badTries = 0;

String readUid() {
  String uid = "";
  for (int i = 0; i < rfid.uid.size; i++) {
    if (i > 0) uid += " ";
    if (rfid.uid.uidByte[i] < 16) uid += "0";
    uid += String(rfid.uid.uidByte[i], HEX);
  }
  uid.toUpperCase();
  return uid;
}

bool isAllowed(String uid) {
  for (int i = 0; i < NUM_ALLOWED; i++) {
    if (uid == allowed[i]) return true;
  }
  return false;
}

void alarm() {
  for (int i = 0; i < 10; i++) {
    digitalWrite(RED_PIN, HIGH);
    tone(BUZZER_PIN, 2000, 150);
    delay(150);
    digitalWrite(RED_PIN, LOW);
    tone(BUZZER_PIN, 1000, 150);
    delay(150);
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  door.attach(SERVO_PIN, 500, 2400);
  door.write(0);
  SPI.begin();
  rfid.PCD_Init();
}

void loop() {
  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;

  String uid = readUid();
  Serial.println(uid);
  if (isAllowed(uid)) {
    badTries = 0;
    digitalWrite(GREEN_PIN, HIGH);
    tone(BUZZER_PIN, 1500, 150);
    door.write(90);
    delay(3000);
    door.write(0);
    digitalWrite(GREEN_PIN, LOW);
  } else {
    badTries++;
    digitalWrite(RED_PIN, HIGH);
    tone(BUZZER_PIN, 200, 800);
    delay(1000);
    digitalWrite(RED_PIN, LOW);
    if (badTries >= 3) {
      alarm();
      badTries = 0;
    }
  }
  rfid.PICC_HaltA();
}
