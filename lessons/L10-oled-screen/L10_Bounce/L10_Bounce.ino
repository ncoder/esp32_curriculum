// Lesson 10: Bouncing ball
// The ball moves a little every frame and bounces off the edges.

#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 display(128, 64, &Wire, -1);

const int R = 4;  // ball radius
int x = 20;
int y = 10;
int dx = 2;  // how far it moves across each frame
int dy = 1;  // how far it moves down each frame

void setup() {
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
}

void loop() {
  x = x + dx;
  y = y + dy;
  if (x <= R || x >= 127 - R) {
    dx = -dx;
  }
  if (y <= R || y >= 63 - R) {
    dy = -dy;
  }
  display.clearDisplay();
  display.drawRect(0, 0, 128, 64, SSD1306_WHITE);
  display.fillCircle(x, y, R, SSD1306_WHITE);
  display.display();
  delay(10);
}
