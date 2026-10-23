// Lesson 18 challenge solution: make your own remote control
// IR transmitter module signal on pin 4, buttons on 13 and 14 (to GND).
// Point it at a friend's ESP32 running L18_RemoteLights.

#include <IRremote.hpp>

const int IR_SEND_PIN_NUM = 4;
const int BUTTON_A = 13;
const int BUTTON_B = 14;

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_A, INPUT_PULLUP);
  pinMode(BUTTON_B, INPUT_PULLUP);
  IrSender.begin(IR_SEND_PIN_NUM);
}

void loop() {
  if (digitalRead(BUTTON_A) == LOW) {
    Serial.println("Sending 1 (red)");
    IrSender.sendNEC(0x00, 0x0C, 0);   // address 0, command 0x0C
    delay(300);
  }
  if (digitalRead(BUTTON_B) == LOW) {
    Serial.println("Sending POWER (off)");
    IrSender.sendNEC(0x00, 0x45, 0);
    delay(300);
  }
}
