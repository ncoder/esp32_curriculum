// Lesson 5 challenge solution: automatic rainbow
// RGB LED on 25/26/27. Smoothly goes round the colour wheel.

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
  for (int i = 0; i < 255; i++) {
    setColor(255 - i, i, 0);
    delay(10);
  }
  for (int i = 0; i < 255; i++) {
    setColor(0, 255 - i, i);
    delay(10);
  }
  for (int i = 0; i < 255; i++) {
    setColor(i, 0, 255 - i);
    delay(10);
  }
}
