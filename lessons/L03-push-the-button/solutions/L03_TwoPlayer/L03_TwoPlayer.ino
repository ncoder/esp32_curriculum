// Lesson 3 challenge solution: two-player reaction game
// Player 1 button on 13 (wins: red LED 25),
// player 2 button on 14 (wins: green LED 27), yellow LED 26 = GO!

const int P1 = 13;
const int P2 = 14;
const int P1_LED = 25;
const int GO_LED = 26;
const int P2_LED = 27;

void setup() {
  Serial.begin(115200);
  pinMode(P1, INPUT_PULLUP);
  pinMode(P2, INPUT_PULLUP);
  pinMode(P1_LED, OUTPUT);
  pinMode(GO_LED, OUTPUT);
  pinMode(P2_LED, OUTPUT);
}

void loop() {
  digitalWrite(P1_LED, LOW);
  digitalWrite(P2_LED, LOW);
  Serial.println("Get ready...");
  delay(random(2000, 6000));
  digitalWrite(GO_LED, HIGH);

  int winnerLed = 0;
  while (winnerLed == 0) {
    if (digitalRead(P1) == LOW) {
      winnerLed = P1_LED;
      Serial.println("Player 1 wins!");
    } else if (digitalRead(P2) == LOW) {
      winnerLed = P2_LED;
      Serial.println("Player 2 wins!");
    }
  }

  digitalWrite(GO_LED, LOW);
  digitalWrite(winnerLed, HIGH);
  delay(3000);
}
