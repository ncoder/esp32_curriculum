// Lesson 17: Access control
// Allowed cards light green and beep once, others red and buzz.

#include <SPI.h>
#include <MFRC522.h>

const int SS_PIN = 5;
const int RST_PIN = 4;
const int RED_PIN = 25;
const int GREEN_PIN = 27;
const int BUZZER_PIN = 33;

// Put your own card UIDs here (copy them from L17_ReadCard)
String allowed[] = {"A3 4F 12 9B", "04 7E 2C 1A"};
const int NUM_ALLOWED = 2;

MFRC522 rfid(SS_PIN, RST_PIN);

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

void setup() {
  Serial.begin(115200);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  SPI.begin();
  rfid.PCD_Init();
}

void loop() {
  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;

  String uid = readUid();
  Serial.print(uid);
  if (isAllowed(uid)) {
    Serial.println("  -> Welcome!");
    digitalWrite(GREEN_PIN, HIGH);
    tone(BUZZER_PIN, 1500, 150);
  } else {
    Serial.println("  -> Access denied");
    digitalWrite(RED_PIN, HIGH);
    tone(BUZZER_PIN, 200, 800);
  }
  delay(2000);
  digitalWrite(GREEN_PIN, LOW);
  digitalWrite(RED_PIN, LOW);
  rfid.PICC_HaltA();
}
