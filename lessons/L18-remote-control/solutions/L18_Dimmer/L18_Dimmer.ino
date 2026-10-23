// Lesson 18 challenge solution: colours + brightness
// 1-5 pick a colour, VOL+ / VOL- change brightness (hold to keep going),
// POWER toggles on/off, 0 starts a rainbow party mode.

#include <IRremote.hpp>

const int IR_PIN = 14;
const int RED_PIN = 25;
const int GREEN_PIN = 26;
const int BLUE_PIN = 27;

int r = 255, g = 255, b = 255;
int brightness = 100;   // percent
bool isOn = true;
bool party = false;

void show() {
  int level = isOn ? brightness : 0;
  analogWrite(RED_PIN, r * level / 100);
  analogWrite(GREEN_PIN, g * level / 100);
  analogWrite(BLUE_PIN, b * level / 100);
}

void pick(int newR, int newG, int newB) {
  r = newR; g = newG; b = newB;
  party = false;
  isOn = true;
}

void setup() {
  Serial.begin(115200);
  IrReceiver.begin(IR_PIN);
  show();
}

void loop() {
  if (IrReceiver.decode()) {
    int code = IrReceiver.decodedIRData.command;
    bool repeat = IrReceiver.decodedIRData.flags & IRDATA_FLAGS_IS_REPEAT;

    switch (code) {
      case 0x0C: if (!repeat) pick(255, 0, 0);     break;
      case 0x18: if (!repeat) pick(0, 255, 0);     break;
      case 0x5E: if (!repeat) pick(0, 0, 255);     break;
      case 0x08: if (!repeat) pick(255, 120, 0);   break;
      case 0x1C: if (!repeat) pick(255, 255, 255); break;
      case 0x16: if (!repeat) party = true;        break;
      case 0x45: if (!repeat) isOn = !isOn;        break;
      case 0x46: brightness = min(brightness + 10, 100); break;
      case 0x15: brightness = max(brightness - 10, 0);   break;
    }
    Serial.print("brightness ");
    Serial.println(brightness);
    IrReceiver.resume();
  }

  if (party && isOn) {
    r = random(256);
    g = random(256);
    b = random(256);
    delay(150);
  }
  show();
}
