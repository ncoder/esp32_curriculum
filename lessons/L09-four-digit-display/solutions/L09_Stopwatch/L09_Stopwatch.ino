// Lesson 9 challenge solution: stopwatch with tenths of a second
// Press: start. Press: stop. Press: reset to 0. Shows 000.0 to 999.9

const int BUTTON_PIN = 13;
const int DP_PIN = 4;
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

void showTenths(int tenths) {
  tenths = constrain(tenths, 0, 9999);
  int divisor = 1000;
  for (int place = 0; place < 4; place++) {
    showDigit(place, tenths / divisor % 10);
    digitalWrite(DP_PIN, place == 2);  // dot after the seconds
    delay(2);
    divisor = divisor / 10;
  }
}

int state = 0;  // 0 = reset, 1 = running, 2 = stopped
unsigned long startTime = 0;
int tenths = 0;
int lastButton = HIGH;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(DP_PIN, OUTPUT);
  for (int s = 0; s < 7; s++) {
    pinMode(segPins[s], OUTPUT);
  }
  for (int d = 0; d < 4; d++) {
    pinMode(digitPins[d], OUTPUT);
  }
}

void loop() {
  int button = digitalRead(BUTTON_PIN);
  if (button == LOW && lastButton == HIGH) {  // just pressed
    if (state == 0) {
      state = 1;
      startTime = millis();
    } else if (state == 1) {
      state = 2;
    } else {
      state = 0;
      tenths = 0;
    }
  }
  lastButton = button;

  if (state == 1) {
    tenths = (millis() - startTime) / 100;
  }
  showTenths(tenths);
}
