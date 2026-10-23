// Lesson 9: Reaction timer game
// When the numbers start counting, press the button as fast as you can!

const int BUTTON_PIN = 13;
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

void showNumber(int number) {
  number = constrain(number, 0, 9999);
  int divisor = 1000;
  for (int place = 0; place < 4; place++) {
    showDigit(place, number / divisor % 10);
    delay(2);
    divisor = divisor / 10;
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  for (int s = 0; s < 7; s++) {
    pinMode(segPins[s], OUTPUT);
  }
  for (int d = 0; d < 4; d++) {
    pinMode(digitPins[d], OUTPUT);
  }
}

void loop() {
  unsigned long goTime = millis() + random(2000, 6000);
  while (millis() < goTime) {
    showNumber(0);  // get ready...
  }
  while (digitalRead(BUTTON_PIN) == HIGH) {
    showNumber(millis() - goTime);  // GO! count until pressed
  }
  int score = millis() - goTime;
  Serial.print("Your time: ");
  Serial.print(score);
  Serial.println(" ms");
  unsigned long showUntil = millis() + 3000;
  while (millis() < showUntil) {
    showNumber(score);
  }
}
