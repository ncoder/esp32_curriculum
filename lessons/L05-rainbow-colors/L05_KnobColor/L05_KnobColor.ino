// Lesson 5: Turn the knob to pick a colour
// RGB LED on 25/26/27, potentiometer middle leg on 34.

const int RED = 25;
const int GREEN = 26;
const int BLUE = 27;
const int KNOB = 34;

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
  int pos = map(analogRead(KNOB), 0, 4095, 0, 764);

  if (pos < 255) {
    setColor(255 - pos, pos, 0);          // red to green
  } else if (pos < 510) {
    pos = pos - 255;
    setColor(0, 255 - pos, pos);          // green to blue
  } else {
    pos = pos - 510;
    setColor(pos, 0, 255 - pos);          // blue to red
  }
  delay(20);
}
