# Hardware notes and pin plan

These notes are for teachers and lesson authors. They record the decisions
every lesson follows, so the same parts end up on the same pins all the way
through the course.

## The board

The kit's board is an ESP32-WROOM-32 dev board with a CP2102 USB chip and a
USB-C socket. In the Arduino IDE, choose **Tools → Board → esp32 → ESP32 Dev
Module** (core: *esp32 by Espressif Systems*, version 3.x). If uploads stall
at `Connecting...`, hold **BOOT** until the upload starts.

The ESP32 runs at **3.3 V**. Its pins must never receive 5 V.

## Which pins we use

| Use | Pins |
|---|---|
| Safe for anything (in/out, PWM) | 4, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33 |
| Input only, no internal pull-up | 34, 35, 36 (VP), 39 (VN) |
| Analog input (ADC1, still works when Wi-Fi is on) | 32, 33, 34, 35, 36, 39 |
| Avoid | 0, 2, 5\*, 12, 15 (boot "strapping" pins); 1, 3 (USB serial); 6–11 (flash memory) |

\* GPIO 5 is used only as the SPI chip-select pin for RFID.

### Standard assignments

| Part | Pin(s) |
|---|---|
| Single LED | 26 |
| Traffic light LEDs | red 25, yellow 26, green 27 |
| RGB LED (common cathode) | R 25, G 26, B 27 |
| Buttons (to GND, `INPUT_PULLUP`) | 13, 14 (piano/extra buttons: 16, 17, 18, 19) |
| Buzzer (active or passive) | 33 |
| Potentiometer | 34 |
| Photoresistor (with 10 kΩ divider) | 35 |
| Joystick | X 34, Y 35, SW 14 |
| I²C (OLED, GY-6500) | SDA 21, SCL 22 |
| SPI (RC522 RFID) | SCK 18, MISO 19, MOSI 23, SDA/SS 5, RST 4 |
| DHT11 | 4 |
| Ultrasonic HC-SR04 | TRIG 17, ECHO 16 (through a 1 kΩ / 2 kΩ divider) |
| PIR HC-SR501 | 27 |
| Servo SG90 | 18 |
| IR receiver | 14 |
| 74HC595 | DATA 23, LATCH 19, CLOCK 18 |

A lesson may change these when it needs a lot of pins (the 7-segment and
keypad lessons do). Each lesson lists its own wiring table.

## Part assumptions

| Part | What we assume | If yours differs |
|---|---|---|
| 0.96" OLED | SSD1306, 128×64, I²C address 0x3C | Try 0x3D. If the picture is shifted or full of noise, it may be an SH1106 |
| 1-digit and 4-digit 7-segment displays | Common cathode (5161AS / 5461AS) | For common anode, flip HIGH/LOW for segments and digits |
| Keypad (membrane switch) | 4×4, keys `123A / 456B / 789C / *0#D` | |
| IR remote | NEC protocol. Lesson 18 first prints the codes, so any remote works | |
| GY-6500 | MPU-6500 accelerometer/gyro at I²C 0x68, read with plain `Wire` | 0x69 if AD0 is high |
| HC-SR04 | 5 V part: ECHO must go through the divider (1 kΩ from ECHO, 2 kΩ to GND, ESP32 pin in the middle) | |
| SG90 servo, HC-SR04, PIR, relay | Powered from the ESP32's **5V/VIN** pin, which is the USB 5 V | |
| DC motor, stepper | Powered from the **power supply module** (set to 5 V), with GND shared with the ESP32 | |
| Buzzers | Active (sealed bottom, beeps on its own) and passive (open bottom, green board, needs `tone()`) | |

## Breadboard layout

The ESP32 board is too wide for one 400-point breadboard. Clip the two
breadboards together and put the ESP32 across the join, one pin row in each
breadboard. One reviewer suggests removing one power rail strip so the two
boards sit flush.
