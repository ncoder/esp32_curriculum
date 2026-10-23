// Lesson 18: Read remote control codes
// IR receiver signal pin on 14. Press buttons and read the codes.

#include <IRremote.hpp>

const int IR_PIN = 14;

void setup() {
  Serial.begin(115200);
  IrReceiver.begin(IR_PIN);
  Serial.println("Press a button on the remote...");
}

void loop() {
  if (IrReceiver.decode()) {
    int code = IrReceiver.decodedIRData.command;
    Serial.print("Button code: 0x");
    Serial.println(code, HEX);
    IrReceiver.resume();
  }
}
