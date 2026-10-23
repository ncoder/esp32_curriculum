# Lesson 19 teacher notes

**About the GY-6500:** it carries an InvenSense **MPU-6500** (accelerometer +
gyro) at I²C address **0x68** (0x69 if AD0 is pulled high). Libraries made
for the MPU-6050 often refuse it because its WHO_AM_I value differs
(0x70 vs 0x68), so we use plain `Wire` reads. This is also a nice lesson in
"registers". The register map for what we use is the same as the MPU-6050:
`0x6B` = PWR_MGMT_1 (write 0 to wake), `0x3B..0x40` = accel X/Y/Z, high byte
first, ±2 g by default (16384 per g).

If a module has headers loose, they must be soldered for reliable readings.

**Common problems**

- *All zeros, or -1 everywhere:* wiring, or the module isn't at 0x68. A quick
  I²C scanner (File → Examples → Wire → WireScan in the esp32 core) shows
  which addresses respond. You should see 0x3C and 0x68.
- *Ball moves the wrong way or on the wrong axis:* depends how the module is
  mounted. Swap `ax`/`ay` or flip signs. Encourage students to reason it out
  from the Serial Plotter.
- *Ball drifts on a flat table:* sensor offset. Students can subtract a
  calibration value read at startup (good extension).
- *OLED blank:* see Lesson 10 (address 0x3C, 3V3 power).

**Quiz answers**

1. z.
2. I²C lets many chips share SDA/SCL; each has its own address (0x3C, 0x68).
3. Both conditions must be true.
4. Phones (screen rotation), Nintendo Switch/Wii controllers, fitness
   trackers, drones, car airbags…

**Challenge solutions:** `solutions/L19_Maze` (challenge 3, with a timer).
Challenge 1: store `unsigned long start = millis();` and check
`millis() - start > 30000`. Challenge 2 reuses the `newDot()` idea with a
second pair of variables.
