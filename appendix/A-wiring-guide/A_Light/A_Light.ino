// Appendix A: test the photoresistor
// 3V3 -> photoresistor -> pin 35 -> 10k resistor -> GND.

const int LIGHT_SENSOR = 35;

void setup() {
  Serial.begin(115200);
}

void loop() {
  int light = analogRead(LIGHT_SENSOR);   // 0 (dark) to 4095 (bright)
  Serial.print("light:");
  Serial.println(light);
  delay(100);
}
