// Lesson 1: Hello, ESP32!
// The ESP32 talks to the computer over the USB cable.

int count = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("Hello! I am an ESP32.");
  Serial.println("My name is: Sparky");
}

void loop() {
  count = count + 1;
  Serial.print("I have counted to ");
  Serial.println(count);
  delay(1000);
}
