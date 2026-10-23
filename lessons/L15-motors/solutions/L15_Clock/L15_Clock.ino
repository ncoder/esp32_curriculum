// Lesson 15 challenge solution: stepper "seconds hand"
// Tape a paper arrow to the stepper shaft. It goes round once a minute.
// 2048 steps / 60 seconds is not a whole number, so we work out
// where the hand should be every second and step until it's there.

const int PINS[4] = {16, 17, 18, 19};
const int PATTERN[4][4] = {
  {1, 1, 0, 0},
  {0, 1, 1, 0},
  {0, 0, 1, 1},
  {1, 0, 0, 1}
};
const int STEPS_PER_TURN = 2048;

int stepNumber = 0;
long position = 0;      // steps taken since the start
long seconds = 0;

void step(int direction) {
  stepNumber = (stepNumber + direction + 4) % 4;
  for (int i = 0; i < 4; i++) {
    digitalWrite(PINS[i], PATTERN[stepNumber][i]);
  }
  delay(3);
}

void allOff() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(PINS[i], LOW);
  }
}

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < 4; i++) {
    pinMode(PINS[i], OUTPUT);
  }
}

void loop() {
  unsigned long start = millis();
  seconds = seconds + 1;
  long target = seconds * STEPS_PER_TURN / 60;
  while (position < target) {
    step(1);
    position = position + 1;
  }
  allOff();
  Serial.println(seconds % 60);

  while (millis() - start < 1000) {
    delay(1);                       // wait out the rest of the second
  }
}
