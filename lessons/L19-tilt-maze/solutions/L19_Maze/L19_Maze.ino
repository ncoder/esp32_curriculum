// Lesson 19 challenge solution: tilt maze with a timer
// Roll the ball from the top-left to the goal square without
// going through walls. Your time is shown when you reach it.

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 display(128, 64, &Wire, -1);

const int IMU = 0x68;
const int BUZZER_PIN = 33;
const int R = 3;   // ball radius

// Walls: x, y, width, height
const int NUM_WALLS = 5;
int walls[NUM_WALLS][4] = {
  {30, 0, 4, 44},
  {60, 20, 4, 44},
  {90, 0, 4, 44},
  {34, 40, 16, 4},
  {94, 20, 16, 4},
};
const int GOAL_X = 112, GOAL_Y = 48, GOAL_SIZE = 12;

int ax, ay, az;
float ballX, ballY;
unsigned long startTime;

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
  Wire.requestFrom(IMU, 6);
  ax = readAxis();
  ay = readAxis();
  az = readAxis();
}

// true if a ball at (x, y) would touch a wall or the screen edge
bool hitsWall(float x, float y) {
  if (x < R || x > 127 - R || y < R || y > 63 - R) return true;
  for (int i = 0; i < NUM_WALLS; i++) {
    int wx = walls[i][0], wy = walls[i][1];
    int ww = walls[i][2], wh = walls[i][3];
    if (x + R > wx && x - R < wx + ww && y + R > wy && y - R < wy + wh) {
      return true;
    }
  }
  return false;
}

void restart() {
  ballX = 10;
  ballY = 10;
  startTime = millis();
}

void setup() {
  Wire.begin();
  Wire.beginTransmission(IMU);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission();
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.setTextColor(WHITE);
  restart();
}

void loop() {
  readAccel();
  float newX = ballX - ax / 2000.0;
  float newY = ballY + ay / 2000.0;
  // Move each direction separately so the ball slides along walls
  if (!hitsWall(newX, ballY)) ballX = newX;
  if (!hitsWall(ballX, newY)) ballY = newY;

  display.clearDisplay();
  for (int i = 0; i < NUM_WALLS; i++) {
    display.fillRect(walls[i][0], walls[i][1], walls[i][2], walls[i][3],
                     WHITE);
  }
  display.drawRect(GOAL_X, GOAL_Y, GOAL_SIZE, GOAL_SIZE, WHITE);
  display.fillCircle(ballX, ballY, R, WHITE);
  display.display();

  if (ballX > GOAL_X && ballY > GOAL_Y) {
    float seconds = (millis() - startTime) / 1000.0;
    tone(BUZZER_PIN, 1000, 100);
    delay(120);
    tone(BUZZER_PIN, 1500, 200);
    display.clearDisplay();
    display.setTextSize(2);
    display.setCursor(10, 10);
    display.print("You win!");
    display.setCursor(10, 36);
    display.print(seconds, 1);
    display.print(" s");
    display.display();
    display.setTextSize(1);
    delay(4000);
    restart();
  }
  delay(20);
}
