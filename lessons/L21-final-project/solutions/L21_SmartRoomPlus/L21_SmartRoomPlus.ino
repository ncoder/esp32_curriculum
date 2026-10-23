// Lesson 21 extension: Smart Room Monitor + phone dashboard
// Everything from L21_SmartRoom, plus:
// - counts how many times someone came in
// - a fan LED (pin 26) switches on automatically when it's too hot
// - a web page at 192.168.4.1 shows the readings (auto-refresh)

#include <WiFi.h>
#include <WebServer.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>

const int DHT_PIN = 4;
const int PIR_PIN = 27;
const int BUZZER_PIN = 33;
const int FAN_LED_PIN = 26;
const float TOO_HOT = 28.0;

String WIFI_NAME = "SmartRoom-ESP32";
String PASSWORD = "smartroom1";

Adafruit_SSD1306 display(128, 64, &Wire, -1);
DHT dht(DHT_PIN, DHT11);
WebServer server(80);

float temp = 0;
float humidity = 0;
unsigned long lastRead = 0;
bool wasMotion = false;
bool motion = false;
int visitors = 0;

void sendPage() {
  String page = "<html><head><meta name='viewport' "
                "content='width=device-width'>"
                "<meta http-equiv='refresh' content='3'></head>"
                "<body style='font-family:sans-serif;text-align:center'>";
  page += "<h1>Smart Room</h1>";
  page += "<p style='font-size:40px'>" + String(temp, 1) + " &deg;C</p>";
  page += "<p>Humidity: " + String(humidity, 0) + " %</p>";
  page += "<p>" + String(motion ? "Someone is here" : "Room is empty") +
          "</p>";
  page += "<p>Visitors today: " + String(visitors) + "</p>";
  if (temp > TOO_HOT) page += "<p style='color:red'>Too hot! Fan on.</p>";
  page += "</body></html>";
  server.send(200, "text/html", page);
}

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
  pinMode(FAN_LED_PIN, OUTPUT);
  dht.begin();
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.setTextColor(WHITE);

  WiFi.softAP(WIFI_NAME, PASSWORD);
  Serial.println(WiFi.softAPIP());
  server.on("/", sendPage);
  server.begin();
}

void loop() {
  server.handleClient();

  if (millis() - lastRead > 2000) {
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    if (!isnan(t)) temp = t;      // ignore failed readings
    if (!isnan(h)) humidity = h;
    lastRead = millis();
  }

  motion = digitalRead(PIR_PIN) == HIGH;
  if (motion && !wasMotion) {
    visitors++;
    tone(BUZZER_PIN, 1200, 150);
    delay(200);
    tone(BUZZER_PIN, 900, 300);
  }
  wasMotion = motion;

  digitalWrite(FAN_LED_PIN, temp > TOO_HOT ? HIGH : LOW);

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
  display.print("Visitors: ");
  display.print(visitors);
  display.setCursor(0, 56);
  display.print(motion ? "Someone is here!" : "Room is empty");
  display.display();
  delay(50);
}
