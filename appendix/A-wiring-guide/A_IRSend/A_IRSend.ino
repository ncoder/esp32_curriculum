// Appendix A: test the IR transmitter
// S on pin 4. Sends the remote's "1" code every second.

#include <IRremote.hpp>

const int IR_SEND_PIN_NUM = 4;

void setup() {
  Serial.begin(115200);
  IrSender.begin(IR_SEND_PIN_NUM);
}

void loop() {
  Serial.println("Sending 1");
  IrSender.sendNEC(0x00, 0x0C, 0);   // address 0, command 0x0C
  delay(1000);
}
