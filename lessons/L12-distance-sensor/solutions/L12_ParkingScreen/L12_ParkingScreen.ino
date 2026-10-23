// Lesson 12 challenge solution: parking sensor with an OLED readout
// OLED on SDA 21 / SCL 22, plus a bar that shrinks as you get closer.

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 display(128, 64, &Wire, -1);

const int TRIG_PIN = 17;
const int ECHO_PIN = 16;
const int BUZZER_PIN = 33;

float readDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long echoTime = pulseIn(ECHO_PIN, HIGH, 30000);
  if (echoTime == 0) {
    return -1;
  }
  return echoTime * 0.0343 / 2;
}

void showDistance(float cm) {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print("Distance");
  display.setTextSize(3);
  display.setCursor(0, 16);
  if (cm < 0) {
    display.print("---");
  } else {
    display.print((int)cm);
    display.setTextSize(1);
    display.print(" cm");
    int bar = constrain(map((int)cm, 0, 50, 0, 128), 0, 128);
    display.fillRect(0, 54, bar, 10, SSD1306_WHITE);
  }
  display.display();
}

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
}

void loop() {
  float cm = readDistance();
  showDistance(cm);

  if (cm < 0 || cm > 50) {
    noTone(BUZZER_PIN);
    delay(200);
  } else if (cm < 5) {
    tone(BUZZER_PIN, 1000);
    delay(100);
  } else {
    tone(BUZZER_PIN, 1000, 60);
    delay(cm * 10);
  }
}
