// Lesson 15: DC motor fan with the L293D chip
// EN (speed) on 25, IN1 on 26, IN2 on 27.

const int EN_PIN = 25;
const int IN1_PIN = 26;
const int IN2_PIN = 27;

void motor(int speed, bool forward) {
  digitalWrite(IN1_PIN, forward);
  digitalWrite(IN2_PIN, !forward);
  analogWrite(EN_PIN, speed);       // 0 = stop, 255 = full speed
}

void setup() {
  Serial.begin(115200);
  pinMode(EN_PIN, OUTPUT);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
}

void loop() {
  Serial.println("Forward, slow");
  motor(150, true);
  delay(3000);

  Serial.println("Forward, fast");
  motor(255, true);
  delay(3000);

  Serial.println("Stop");
  motor(0, true);
  delay(2000);

  Serial.println("Backward");
  motor(200, false);
  delay(3000);

  Serial.println("Stop");
  motor(0, true);
  delay(2000);
}
