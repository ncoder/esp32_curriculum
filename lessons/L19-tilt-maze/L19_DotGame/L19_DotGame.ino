// Lesson 19: Rolling ball
// Tilt the breadboard to roll a ball around the OLED screen.

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 display(128, 64, &Wire, -1);

const int IMU = 0x68;
int ax, ay;
float ballX = 64;
float ballY = 32;
const int BUZZER_PIN = 33;
int dotX, dotY;
int score = 0;

int readAxis() {
  int high = Wire.read();
  int low = Wire.read();
  int value = high * 256 + low;
  if (value > 32767) value = value - 65536;
  return value;
}

void readAccel() {
  Wire.beginTransmission(IMU);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(IMU, 4);
  ax = readAxis();
  ay = readAxis();
}

void newDot() {
  dotX = random(8, 120);
  dotY = random(12, 56);
}

void setup() {
  Wire.begin();
  Wire.beginTransmission(IMU);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission();
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.setTextColor(WHITE);
  newDot();
}

void loop() {
  readAccel();
  ballX = ballX - ax / 2000.0;   // wrong way? change - to +
  ballY = ballY + ay / 2000.0;
  ballX = constrain(ballX, 3, 124);
  ballY = constrain(ballY, 3, 60);

  if (abs(ballX - dotX) < 5 && abs(ballY - dotY) < 5) {
    score = score + 1;
    tone(BUZZER_PIN, 1500, 60);
    newDot();
  }

  display.clearDisplay();
  display.drawRect(0, 0, 128, 64, WHITE);
  display.setCursor(4, 4);
  display.print(score);
  display.drawCircle(dotX, dotY, 2, WHITE);
  display.fillCircle(ballX, ballY, 3, WHITE);
  display.display();
  delay(20);
}
