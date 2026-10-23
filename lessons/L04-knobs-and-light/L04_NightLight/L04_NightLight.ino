// Lesson 4: Automatic night light
// Photoresistor from 3V3 to pin 35, 10k resistor from 35 to GND.
// The green LED on 27 comes on when it gets dark.

const int LIGHT_SENSOR = 35;
const int LED = 27;
const int DARK = 1500;   // change this to suit your room

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
}

void loop() {
  int light = analogRead(LIGHT_SENSOR);
  Serial.print("light:");
  Serial.println(light);

  if (light < DARK) {
    digitalWrite(LED, HIGH);
  } else {
    digitalWrite(LED, LOW);
  }
  delay(100);
}
