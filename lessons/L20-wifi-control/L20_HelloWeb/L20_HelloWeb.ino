// Lesson 20: Hello, web!
// The ESP32 makes its own Wi-Fi network and serves a web page.

#include <WiFi.h>
#include <WebServer.h>

String WIFI_NAME = "Sparky-ESP32";   // make this unique!
String PASSWORD = "secret123";       // at least 8 characters
const int POT_PIN = 34;

WebServer server(80);

void handleRoot() {
  String page = "<html><body style='font-family:sans-serif'>";
  page += "<h1>Hello from my ESP32!</h1>";
  page += "<p>Knob reading: ";
  page += analogRead(POT_PIN);
  page += "</p></body></html>";
  server.send(200, "text/html", page);
}

void setup() {
  Serial.begin(115200);
  WiFi.softAP(WIFI_NAME, PASSWORD);
  Serial.print("Join Wi-Fi ");
  Serial.print(WIFI_NAME);
  Serial.print(" then open http://");
  Serial.println(WiFi.softAPIP());

  server.on("/", handleRoot);
  server.begin();
}

void loop() {
  server.handleClient();
}
