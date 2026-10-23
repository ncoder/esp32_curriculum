// Lesson 10: Hello, screen!
// OLED screen: SDA on pin 21, SCL on pin 22.

#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 display(128, 64, &Wire, -1);

int count = 0;

void setup() {
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
}

void loop() {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("Hello, I am Sparky!");
  display.setTextSize(3);
  display.setCursor(0, 24);
  display.println(count);
  display.display();
  count = count + 1;
  delay(500);
}
