// Appendix A: thermometer made from the thermistor
// 3V3 -> 10k resistor -> pin 34 -> thermistor -> GND.

const int THERM_PIN = 34;
const float B = 3950;   // the thermistor's "B value"

void setup() {
  Serial.begin(115200);
}

void loop() {
  int mv = analogReadMilliVolts(THERM_PIN);
  float resistance = 10000.0 * mv / (3300 - mv);
  float kelvin = 1 / (1 / 298.15 + log(resistance / 10000) / B);
  float celsius = kelvin - 273.15;

  Serial.print("Temperature: ");
  Serial.print(celsius, 1);
  Serial.println(" C");
  delay(1000);
}
