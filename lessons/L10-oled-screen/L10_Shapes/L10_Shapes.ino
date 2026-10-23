// Lesson 10: Draw with shapes
// A robot face that blinks. x goes 0-127 across, y goes 0-63 down.

#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 display(128, 64, &Wire, -1);

void drawEyes(int color) {
  display.fillCircle(48, 30, 7, color);
  display.fillCircle(80, 30, 7, color);
}

void setup() {
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.drawRoundRect(24, 10, 80, 53, 8, SSD1306_WHITE);  // head
  display.drawLine(64, 10, 64, 3, SSD1306_WHITE);           // antenna
  display.fillCircle(64, 3, 3, SSD1306_WHITE);
  display.fillTriangle(64, 36, 59, 44, 69, 44, SSD1306_WHITE);
  display.drawRect(46, 50, 36, 7, SSD1306_WHITE);           // mouth
  drawEyes(SSD1306_WHITE);
  display.display();
}

void loop() {
  delay(3000);
  drawEyes(SSD1306_BLACK);  // close the eyes
  display.drawLine(41, 30, 55, 30, SSD1306_WHITE);
  display.drawLine(73, 30, 87, 30, SSD1306_WHITE);
  display.display();
  delay(200);
  drawEyes(SSD1306_WHITE);  // open them again
  display.display();
}
