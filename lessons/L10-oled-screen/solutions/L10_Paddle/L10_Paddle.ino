// Lesson 10 bonus solution: paddle game
// Turn the knob (pin 34) to move the paddle. Don't let the ball fall!

#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 display(128, 64, &Wire, -1);

const int POT_PIN = 34;
const int R = 3;
const int PADDLE_W = 24;
int x = 64;
int y = 10;
int dx = 2;
int dy = 2;
int score = 0;

void setup() {
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.setTextColor(SSD1306_WHITE);
}

void loop() {
  int paddleX = map(analogRead(POT_PIN), 0, 4095, 0, 128 - PADDLE_W);

  x = x + dx;
  y = y + dy;
  if (x <= R || x >= 127 - R) {
    dx = -dx;
  }
  if (y <= R + 8) {
    dy = -dy;
  }
  if (y >= 58 - R && x >= paddleX && x <= paddleX + PADDLE_W) {
    dy = -dy;  // hit the paddle
    score = score + 1;
  }
  if (y > 63) {  // missed: start again
    score = 0;
    x = 64;
    y = 10;
    delay(500);
  }

  display.clearDisplay();
  display.setCursor(0, 0);
  display.print("Score: ");
  display.print(score);
  display.fillCircle(x, y, R, SSD1306_WHITE);
  display.fillRect(paddleX, 59, PADDLE_W, 4, SSD1306_WHITE);
  display.display();
  delay(15);
}
