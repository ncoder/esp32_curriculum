// Lesson 11 challenge solution: thermometer made from a thermistor
// 3V3 -> 10k resistor -> pin 34 -> thermistor -> GND.
// Assumes a 10k NTC thermistor with a "B value" of 3950.

#include <DHT.h>

const int THERM_PIN = 34;
const float B = 3950;

DHT dht(4, DHT11);

void setup() {
  Serial.begin(115200);
  dht.begin();
}

void loop() {
  int mv = analogReadMilliVolts(THERM_PIN);
  float resistance = 10000.0 * mv / (3300 - mv);
  float kelvin = 1 / (1 / 298.15 + log(resistance / 10000) / B);
  float celsius = kelvin - 273.15;

  Serial.print("Thermistor: ");
  Serial.print(celsius, 1);
  Serial.print(" C   DHT11: ");
  Serial.print(dht.readTemperature(), 1);
  Serial.println(" C");
  delay(2000);
}
