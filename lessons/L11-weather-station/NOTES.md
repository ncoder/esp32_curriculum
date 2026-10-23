# Lesson 11 teacher notes

**Before class:** install **DHT sensor library** (Adafruit) together with
**Adafruit Unified Sensor**. The OLED from Lesson 10 should still be wired.
The DHT11 module in the kit has its own pull-up resistor, so no extra
resistor is needed. Its pin labels vary (S/+/–, or DATA/VCC/GND, and the
middle pin is usually VCC); make students read them.

**About the readings:** the DHT11 is a basic sensor: ±2 °C and ±5 %RH, and
it reads only once every 1–2 seconds. Several sensors in the same room will
disagree by a degree or two. That makes a good discussion about accuracy.
Breathing on it raises the humidity by 20–40 % within a few seconds, and it
falls back within a minute.

**Common problems**

- *`Could not read the sensor!` / NaN:* the signal wire isn't on pin 4, the
  sensor isn't powered, or the reading came too soon after power-up.
- *Compile error `Adafruit_Sensor.h: No such file`:* the *Adafruit Unified
  Sensor* dependency wasn't installed.
- *L11_Comfort shows `nan C` with a happy face:* the sensor failed. NaN makes
  every comparison false, so the message stays "Just right!". Ask a strong
  student to add the `isnan` check from L11_Station.
- *Screen blank after adding the DHT:* the OLED wires were disturbed.
  L10_Hello is a quick test.

**Quiz answers**

1. Temperature and humidity.
2. An `int` is a whole number; a `float` can have a decimal point.
3. Breath is warm and full of water vapour.

**Challenge solutions:** `solutions/L11_MinMax` (challenge 2) and
`solutions/L11_Thermistor` (bonus). The thermistor solution assumes a 10 kΩ
NTC thermistor with B = 3950, which is what ELEGOO kits usually include. If
readings are off by several degrees, adjust `B`. For challenge 1, use
`dht.readTemperature(true)`. For challenge 3, add `pinMode(26, OUTPUT)`
and `digitalWrite(26, message == "Too hot!")`.
