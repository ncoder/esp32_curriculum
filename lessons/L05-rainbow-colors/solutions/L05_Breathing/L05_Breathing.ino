// Lesson 5 challenge solution: breathing light, button picks colour
// RGB LED on 25/26/27, button on 13 (other leg to GND).

const int RED = 25;
const int GREEN = 26;
const int BLUE = 27;
const int BUTTON = 13;

int colors[4][3] = {
  {255, 0, 0}, {0, 255, 0}, {0, 0, 255}, {128, 0, 255}
};
int current = 0;

void setColor(int r, int g, int b) {
  analogWrite(RED, r);
  analogWrite(GREEN, g);
  analogWrite(BLUE, b);
}

void show(int level) {
  setColor(colors[current][0] * level / 255,
           colors[current][1] * level / 255,
           colors[current][2] * level / 255);
  delay(6);
}

void setup() {
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
  pinMode(BUTTON, INPUT_PULLUP);
}

void loop() {
  for (int level = 0; level <= 255; level++) {
    show(level);
  }
  for (int level = 255; level >= 0; level--) {
    show(level);
  }
  if (digitalRead(BUTTON) == LOW) {
    current = (current + 1) % 4;
  }
}
