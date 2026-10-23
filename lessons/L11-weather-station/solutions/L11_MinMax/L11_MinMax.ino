// Lesson 11 challenge solution: lowest and highest temperature
// Remembers the coldest and hottest reading since the ESP32 started.

#include <DHT.h>
#include <Adafruit_SSD1306.h>

DHT dht(4, DHT11);
Adafruit_SSD1306 display(128, 64, &Wire, -1);

float lowest = 100;
float highest = -100;

void setup() {
  dht.begin();
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.setTextColor(SSD1306_WHITE);
}

void loop() {
  float temp = dht.readTemperature();
  if (!isnan(temp)) {
    if (temp < lowest) {
      lowest = temp;
    }
    if (temp > highest) {
      highest = temp;
    }
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("Temperature");
  display.setTextSize(2);
  display.setCursor(0, 14);
  display.print(temp, 1);
  display.println(" C");
  display.setTextSize(1);
  display.setCursor(0, 44);
  display.print("Lowest:  ");
  display.println(lowest, 1);
  display.print("Highest: ");
  display.println(highest, 1);
  display.display();
  delay(2000);
}
