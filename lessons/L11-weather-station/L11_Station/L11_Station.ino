// Lesson 11: Weather station
// DHT11 on pin 4, OLED screen on pins 21 (SDA) and 22 (SCL).

#include <DHT.h>
#include <Adafruit_SSD1306.h>

DHT dht(4, DHT11);
Adafruit_SSD1306 display(128, 64, &Wire, -1);

void setup() {
  dht.begin();
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.setTextColor(SSD1306_WHITE);
}

void loop() {
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();

  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("Weather station");
  if (isnan(temp) || isnan(humidity)) {
    display.println("Sensor error!");
  } else {
    display.setTextSize(2);
    display.setCursor(0, 18);
    display.print(temp, 1);
    display.print(" C");
    display.setCursor(0, 42);
    display.print(humidity, 0);
    display.print(" %");
  }
  display.display();
  delay(2000);
}
