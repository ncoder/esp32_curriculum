// Appendix A: click the relay on and off
// Relay board: S on pin 32, + to VIN (5 V). It switches the red LED.

const int RELAY_PIN = 32;

void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
}

void loop() {
  digitalWrite(RELAY_PIN, HIGH);   // click: LED on
  Serial.println("relay ON");
  delay(1000);
  digitalWrite(RELAY_PIN, LOW);    // clack: LED off
  Serial.println("relay OFF");
  delay(1000);
}
