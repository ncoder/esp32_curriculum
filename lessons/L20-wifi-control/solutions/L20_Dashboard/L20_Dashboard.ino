// Lesson 20 challenge solution: phone dashboard
// - page refreshes itself every 2 seconds
// - big styled buttons for the LED, plus a BEEP button (buzzer on 33)
// - a slider-free brightness control using links /dim?level=0..255

#include <WiFi.h>
#include <WebServer.h>

String WIFI_NAME = "Sparky-ESP32";
String PASSWORD = "secret123";
const int POT_PIN = 34;
const int LED_PIN = 26;
const int BUZZER_PIN = 33;

WebServer server(80);
int brightness = 0;

String button(String url, String label, String color) {
  return "<a href='" + url + "'><button style='font-size:24px;"
         "padding:12px 24px;margin:6px;background:" + color +
         ";color:white;border:none;border-radius:8px'>" + label +
         "</button></a>";
}

void sendPage() {
  int knob = analogRead(POT_PIN);
  String page = "<html><head><meta name='viewport' "
                "content='width=device-width'>"
                "<meta http-equiv='refresh' content='2; url=/'>"
                "</head><body style='font-family:sans-serif;"
                "text-align:center'>";
  page += "<h1>My ESP32 Dashboard</h1>";
  page += "<p>Knob: " + String(knob) + "</p>";
  // A bar that grows with the knob
  page += "<div style='background:#ddd;width:80%;margin:auto'>"
          "<div style='background:#00838f;height:24px;width:" +
          String(knob * 100 / 4095) + "%'></div></div>";
  page += "<p>LED brightness: " + String(brightness) + "</p>";
  page += button("/dim?level=0", "OFF", "#555");
  page += button("/dim?level=40", "LOW", "#e8590c");
  page += button("/dim?level=255", "HIGH", "#2f9e44");
  page += "<br>" + button("/beep", "BEEP!", "#7048e8");
  page += "</body></html>";
  server.send(200, "text/html", page);
}

void redirectHome() {
  server.sendHeader("Location", "/");
  server.send(303);
}

void handleDim() {
  brightness = constrain(server.arg("level").toInt(), 0, 255);
  analogWrite(LED_PIN, brightness);
  redirectHome();
}

void handleBeep() {
  tone(BUZZER_PIN, 1000, 300);
  redirectHome();
}

void setup() {
  Serial.begin(115200);
  WiFi.softAP(WIFI_NAME, PASSWORD);
  Serial.print("Open http://");
  Serial.println(WiFi.softAPIP());

  server.on("/", sendPage);
  server.on("/dim", handleDim);
  server.on("/beep", handleBeep);
  server.begin();
}

void loop() {
  server.handleClient();
}
