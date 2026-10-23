// Lesson 1 challenge solution: flash SOS in Morse code (... --- ...)

const int LED_PIN = 26;

void flash(int onTime) {
  digitalWrite(LED_PIN, HIGH);
  delay(onTime);
  digitalWrite(LED_PIN, LOW);
  delay(200);
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  flash(200); flash(200); flash(200);   // S
  delay(300);
  flash(600); flash(600); flash(600);   // O
  delay(300);
  flash(200); flash(200); flash(200);   // S
  delay(1500);
}
