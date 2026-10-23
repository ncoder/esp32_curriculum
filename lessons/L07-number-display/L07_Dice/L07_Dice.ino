// Lesson 7: Electronic dice
// Press the button on pin 13 to roll.

const int BUTTON_PIN = 13;
const int segPins[7] = {23, 22, 21, 19, 18, 17, 16};

const int digits[10][7] = {
// a  b  c  d  e  f  g
  {1, 1, 1, 1, 1, 1, 0},  // 0
  {0, 1, 1, 0, 0, 0, 0},  // 1
  {1, 1, 0, 1, 1, 0, 1},  // 2
  {1, 1, 1, 1, 0, 0, 1},  // 3
  {0, 1, 1, 0, 0, 1, 1},  // 4
  {1, 0, 1, 1, 0, 1, 1},  // 5
  {1, 0, 1, 1, 1, 1, 1},  // 6
  {1, 1, 1, 0, 0, 0, 0},  // 7
  {1, 1, 1, 1, 1, 1, 1},  // 8
  {1, 1, 1, 1, 0, 1, 1}   // 9
};

void showDigit(int n) {
  for (int s = 0; s < 7; s++) {
    digitalWrite(segPins[s], digits[n][s]);
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  for (int s = 0; s < 7; s++) {
    pinMode(segPins[s], OUTPUT);
  }
  showDigit(0);
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    for (int i = 0; i < 12; i++) {  // rolling animation
      showDigit(random(1, 7));
      delay(40 + i * 15);
    }
    int roll = random(1, 7);
    showDigit(roll);
    Serial.print("You rolled a ");
    Serial.println(roll);
    while (digitalRead(BUTTON_PIN) == LOW) {
      delay(10);  // wait until the button is let go
    }
  }
}
