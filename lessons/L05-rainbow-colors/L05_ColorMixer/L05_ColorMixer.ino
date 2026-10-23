// Lesson 5: Mix colours with an RGB LED
// RGB LED: red 25, green 26, blue 27 (220 ohm each), long leg GND.

const int RED = 25;
const int GREEN = 26;
const int BLUE = 27;

void setColor(int r, int g, int b) {
  analogWrite(RED, r);
  analogWrite(GREEN, g);
  analogWrite(BLUE, b);
}

void setup() {
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
}

void loop() {
  setColor(255, 0, 0);      // red
  delay(1000);
  setColor(0, 255, 0);      // green
  delay(1000);
  setColor(0, 0, 255);      // blue
  delay(1000);
  setColor(255, 255, 0);    // yellow
  delay(1000);
  setColor(128, 0, 255);    // purple
  delay(1000);
  setColor(255, 255, 255);  // white
  delay(1000);
}
