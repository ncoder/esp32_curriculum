// Lesson 11: Comfort face
// A smiley face when the room is comfortable, a sad face when not.

#include <DHT.h>
#include <Adafruit_SSD1306.h>

DHT dht(4, DHT11);
Adafruit_SSD1306 display(128, 64, &Wire, -1);

void drawFace(bool happy) {
  if (happy) {
    display.fillCircle(100, 38, 10, SSD1306_WHITE);  // smile
    display.fillCircle(100, 34, 10, SSD1306_BLACK);
  } else {
    display.fillCircle(100, 52, 10, SSD1306_WHITE);  // frown
    display.fillCircle(100, 56, 10, SSD1306_BLACK);
  }
  display.drawCircle(100, 36, 22, SSD1306_WHITE);
  display.fillCircle(92, 28, 3, SSD1306_WHITE);
  display.fillCircle(108, 28, 3, SSD1306_WHITE);
}

void setup() {
  dht.begin();
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.setTextColor(SSD1306_WHITE);
}

void loop() {
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();

  String message = "Just right!";
  if (temp > 26) {
    message = "Too hot!";
  } else if (temp < 18) {
    message = "Too cold!";
  } else if (humidity > 60) {
    message = "Too damp!";
  } else if (humidity < 30) {
    message = "Too dry!";
  }

  display.clearDisplay();
  display.setTextSize(2);
  display.setCursor(0, 4);
  display.print(temp, 0);
  display.println(" C");
  display.print(humidity, 0);
  display.println(" %");
  display.setTextSize(1);
  display.setCursor(0, 52);
  display.print(message);
  drawFace(message == "Just right!");
  display.display();
  delay(2000);
}
