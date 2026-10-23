// Lesson 15: Stepper motor
// ULN2003 board IN1-IN4 on pins 16, 17, 18, 19.

const int PINS[4] = {16, 17, 18, 19};
const int PATTERN[4][4] = {
  {1, 1, 0, 0},
  {0, 1, 1, 0},
  {0, 0, 1, 1},
  {1, 0, 0, 1}
};
const int STEPS_PER_TURN = 2048;

int stepNumber = 0;

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
  Serial.println("One full turn forwards");
  for (int i = 0; i < STEPS_PER_TURN; i++) {
    step(1);
  }
  allOff();
  delay(1000);

  Serial.println("Quarter turn backwards");
  for (int i = 0; i < STEPS_PER_TURN / 4; i++) {
    step(-1);
  }
  allOff();
  delay(1000);
}
