// Lesson 9: Four digits, one at a time
// Shows 1234 by lighting each digit in turn, very fast.

const int segPins[7] = {23, 22, 21, 19, 18, 17, 16};
const int digitPins[4] = {25, 26, 27, 32};

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

void showDigit(int place, int n) {
  for (int d = 0; d < 4; d++) {
    digitalWrite(digitPins[d], HIGH);  // all digits off
  }
  for (int s = 0; s < 7; s++) {
    digitalWrite(segPins[s], digits[n][s]);
  }
  digitalWrite(digitPins[place], LOW);  // this digit on
}

void setup() {
  for (int s = 0; s < 7; s++) {
    pinMode(segPins[s], OUTPUT);
  }
  for (int d = 0; d < 4; d++) {
    pinMode(digitPins[d], OUTPUT);
  }
}

void loop() {
  showDigit(0, 1);
  delay(5);
  showDigit(1, 2);
  delay(5);
  showDigit(2, 3);
  delay(5);
  showDigit(3, 4);
  delay(5);
}
