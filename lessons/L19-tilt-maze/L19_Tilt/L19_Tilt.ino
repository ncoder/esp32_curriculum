// Lesson 19: Read the tilt sensor
// GY-6500 on I2C (SDA 21, SCL 22). Open the Serial Plotter!

#include <Wire.h>

const int IMU = 0x68;
int ax, ay, az;

int readAxis() {
  int high = Wire.read();
  int low = Wire.read();
  int value = high * 256 + low;
  if (value > 32767) value = value - 65536;
  return value;
}

void readAccel() {
  Wire.beginTransmission(IMU);
  Wire.write(0x3B);              // first accelerometer register
  Wire.endTransmission(false);
  Wire.requestFrom(IMU, 6);
  ax = readAxis();
  ay = readAxis();
  az = readAxis();
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  Wire.beginTransmission(IMU);
  Wire.write(0x6B);              // power register
  Wire.write(0);                 // 0 = wake up!
  Wire.endTransmission();
}

void loop() {
  readAccel();
  Serial.print("x:");
  Serial.print(ax);
  Serial.print(" y:");
  Serial.print(ay);
  Serial.print(" z:");
  Serial.println(az);
  delay(100);
}
