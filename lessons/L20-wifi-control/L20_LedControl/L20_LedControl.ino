// Lesson 20: Control an LED from your phone
// Buttons on the web page switch the LED on pin 26.

#include <WiFi.h>
#include <WebServer.h>

String WIFI_NAME = "Sparky-ESP32";
String PASSWORD = "secret123";
const int POT_PIN = 34;
const int LED_PIN = 26;

WebServer server(80);
bool ledOn = false;

void sendPage() {
  String page = "<html><head><meta name='viewport' ";
  page += "content='width=device-width'></head>";
  page += "<body style='font-family:sans-serif;text-align:center'>";
  page += "<h1>My ESP32</h1>";
  page += "<p>LED is ";
  if (ledOn) page += "ON";
  else page += "OFF";
  page += "</p><p>Knob: ";
  page += analogRead(POT_PIN);
  page += "</p>";
  page += "<a href='/on'><button>ON</button></a> ";
  page += "<a href='/off'><button>OFF</button></a>";
  page += "</body></html>";
  server.send(200, "text/html", page);
}

void handleOn() {
  ledOn = true;
  digitalWrite(LED_PIN, HIGH);
  sendPage();
}

void handleOff() {
  ledOn = false;
  digitalWrite(LED_PIN, LOW);
  sendPage();
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  WiFi.softAP(WIFI_NAME, PASSWORD);
  Serial.println(WiFi.softAPIP());

  server.on("/", sendPage);
  server.on("/on", handleOn);
  server.on("/off", handleOff);
  server.begin();
}

void loop() {
  server.handleClient();
}
