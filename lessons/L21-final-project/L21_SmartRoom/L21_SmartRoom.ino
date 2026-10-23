// Lesson 21: Example project - Smart Room Monitor
// DHT11 on 4, PIR on 27, buzzer on 33, OLED on 21/22.

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>

const int DHT_PIN = 4;
const int PIR_PIN = 27;
const int BUZZER_PIN = 33;
const float TOO_HOT = 28.0;

Adafruit_SSD1306 display(128, 64, &Wire, -1);
DHT dht(DHT_PIN, DHT11);

float temp = 0;
float humidity = 0;
unsigned long lastRead = 0;
bool wasMotion = false;

void setup() {
  pinMode(PIR_PIN, INPUT);
  dht.begin();
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.setTextColor(WHITE);
}

void loop() {
  // 1. Read the DHT11 every 2 seconds (it is slow)
  if (millis() - lastRead > 2000) {
    temp = dht.readTemperature();
    humidity = dht.readHumidity();
    lastRead = millis();
  }

  // 2. Ding-dong when someone walks in
  bool motion = digitalRead(PIR_PIN) == HIGH;
  if (motion && !wasMotion) {
    tone(BUZZER_PIN, 1200, 150);
    delay(200);
    tone(BUZZER_PIN, 900, 300);
  }
  wasMotion = motion;

  // 3. Show everything on the screen
  display.clearDisplay();
  display.setTextSize(2);
  display.setCursor(0, 0);
  display.print(temp, 1);
  display.print(" C");
  display.setCursor(0, 20);
  display.print(humidity, 0);
  display.print(" %");
  display.setTextSize(1);
  display.setCursor(0, 44);
  if (temp > TOO_HOT) display.print("Too hot! Open a window");
  display.setCursor(0, 56);
  if (motion) display.print("Someone is here!");
  else display.print("Room is empty");
  display.display();
  delay(100);
}
