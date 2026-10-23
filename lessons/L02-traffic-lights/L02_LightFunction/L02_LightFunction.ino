// Lesson 2: Traffic light with our own function
// Same wiring as L02_TrafficLight.

const int RED = 25;
const int YELLOW = 26;
const int GREEN = 27;

void lights(int r, int y, int g, int wait) {
  digitalWrite(RED, r);
  digitalWrite(YELLOW, y);
  digitalWrite(GREEN, g);
  delay(wait);
}

void setup() {
  pinMode(RED, OUTPUT);
  pinMode(YELLOW, OUTPUT);
  pinMode(GREEN, OUTPUT);
}

void loop() {
  lights(HIGH, LOW, LOW, 3000);   // stop
  lights(LOW, LOW, HIGH, 3000);   // go
  lights(LOW, HIGH, LOW, 1000);   // get ready to stop
}
