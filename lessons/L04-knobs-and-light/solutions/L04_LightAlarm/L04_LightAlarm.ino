// Lesson 4 challenge solution: secret drawer alarm
// Put the circuit in a dark box. If someone opens it and light
// gets in, the red LED on 25 flashes.

const int LIGHT_SENSOR = 35;
const int RED = 25;
const int BRIGHT = 2000;   // change this to suit your box

void setup() {
  Serial.begin(115200);
  pinMode(RED, OUTPUT);
}

void loop() {
  int light = analogRead(LIGHT_SENSOR);

  if (light > BRIGHT) {
    Serial.println("Intruder! Someone opened the box!");
    for (int i = 0; i < 10; i++) {
      digitalWrite(RED, HIGH);
      delay(100);
      digitalWrite(RED, LOW);
      delay(100);
    }
  }
  delay(100);
}
