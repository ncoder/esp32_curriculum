// Lesson 17: Read an RFID card
// RC522 reader on SPI: SCK 18, MISO 19, MOSI 23, SDA 5, RST 4.

#include <SPI.h>
#include <MFRC522.h>

const int SS_PIN = 5;
const int RST_PIN = 4;

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

void setup() {
  Serial.begin(115200);
  SPI.begin();
  rfid.PCD_Init();
  Serial.println("Hold a card or tag near the reader...");
}

void loop() {
  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;

  Serial.print("Card UID: ");
  Serial.println(readUid());
  rfid.PICC_HaltA();
}
