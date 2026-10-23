// Lesson 16: Read the keypad
// Rows on 13, 14, 27, 26. Columns on 25, 4, 16, 17. Buzzer on 33.

#include <Keypad.h>

const byte ROWS = 4;
const byte COLS = 4;
char keys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};
byte rowPins[ROWS] = {13, 14, 27, 26};
byte colPins[COLS] = {25, 4, 16, 17};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

const int BUZZER_PIN = 33;

void setup() {
  Serial.begin(115200);
  Serial.println("Press some keys!");
}

void loop() {
  char key = keypad.getKey();
  if (key) {
    Serial.print("You pressed: ");
    Serial.println(key);
    tone(BUZZER_PIN, 1500, 50);
  }
}
