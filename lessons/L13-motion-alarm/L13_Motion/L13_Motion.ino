// Lesson 13: Motion detector
// PIR sensor on pin 27, LED on pin 26.

const int PIR_PIN = 27;
const int LED_PIN = 26;

int count = 0;
bool wasMoving = false;

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("Warming up... keep still for 1 minute!");
}

void loop() {
  bool moving = digitalRead(PIR_PIN) == HIGH;
  digitalWrite(LED_PIN, moving);

  if (moving && !wasMoving) {       // it just started
    count = count + 1;
    Serial.print("Motion! Count: ");
    Serial.println(count);
  }
  if (!moving && wasMoving) {       // it just stopped
    Serial.println("All quiet.");
  }

  wasMoving = moving;
  delay(50);
}
