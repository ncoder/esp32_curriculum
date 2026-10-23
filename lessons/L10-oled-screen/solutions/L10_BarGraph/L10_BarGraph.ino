// Lesson 10 challenge solution: knob meter
// Potentiometer on pin 34. Shows a percentage and a bar.

#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 display(128, 64, &Wire, -1);

const int POT_PIN = 34;

void setup() {
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.setTextColor(SSD1306_WHITE);
}

void loop() {
  int percent = map(analogRead(POT_PIN), 0, 4095, 0, 100);
  int barWidth = map(percent, 0, 100, 0, 124);

  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("Knob position");
  display.setTextSize(2);
  display.setCursor(0, 16);
  display.print(percent);
  display.println("%");
  display.drawRect(0, 44, 128, 16, SSD1306_WHITE);
  display.fillRect(2, 46, barWidth, 12, SSD1306_WHITE);
  display.display();
  delay(30);
}
