// Lesson 18: Remote control lights
// Buttons 1-5 pick a colour on the RGB LED, POWER turns it off.

#include <IRremote.hpp>

const int IR_PIN = 14;
const int RED_PIN = 25;
const int GREEN_PIN = 26;
const int BLUE_PIN = 27;

void color(int r, int g, int b) {
  analogWrite(RED_PIN, r);
  analogWrite(GREEN_PIN, g);
  analogWrite(BLUE_PIN, b);
}

void setup() {
  Serial.begin(115200);
  IrReceiver.begin(IR_PIN);
  color(0, 0, 0);
}

void loop() {
  if (IrReceiver.decode()) {
    int code = IrReceiver.decodedIRData.command;
    Serial.println(code, HEX);

    switch (code) {
      case 0x0C: color(255, 0, 0);     break;  // 1 = red
      case 0x18: color(0, 255, 0);     break;  // 2 = green
      case 0x5E: color(0, 0, 255);     break;  // 3 = blue
      case 0x08: color(255, 120, 0);   break;  // 4 = yellow
      case 0x1C: color(255, 255, 255); break;  // 5 = white
      case 0x45: color(0, 0, 0);       break;  // POWER = off
    }
    IrReceiver.resume();
  }
}
