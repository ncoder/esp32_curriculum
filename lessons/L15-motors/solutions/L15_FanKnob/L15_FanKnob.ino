// Lesson 15 challenge solution: fan speed knob
// Potentiometer on 34. Middle = stop, turn right = forwards,
// turn left = backwards. The further you turn, the faster it goes.

const int EN_PIN = 25;
const int IN1_PIN = 26;
const int IN2_PIN = 27;
const int POT_PIN = 34;

void motor(int speed, bool forward) {
  digitalWrite(IN1_PIN, forward);
  digitalWrite(IN2_PIN, !forward);
  analogWrite(EN_PIN, speed);
}

void setup() {
  Serial.begin(115200);
  pinMode(EN_PIN, OUTPUT);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
}

void loop() {
  int knob = analogRead(POT_PIN);

  if (knob > 2300) {
    int speed = map(knob, 2300, 4095, 100, 255);
    motor(speed, true);
    Serial.print("Forwards ");
    Serial.println(speed);
  } else if (knob < 1800) {
    int speed = map(knob, 1800, 0, 100, 255);
    motor(speed, false);
    Serial.print("Backwards ");
    Serial.println(speed);
  } else {
    motor(0, true);
    Serial.println("Stop");
  }
  delay(100);
}
