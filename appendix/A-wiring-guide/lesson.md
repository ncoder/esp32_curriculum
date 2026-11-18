---
appendix: A
title: Wiring guide, part by part
tagline: How to wire up each part in the kit on its own, and where to find it in the lessons.
---

## How to use this guide

Every major part in the kit is listed below, in the same groups as the lessons. If a lesson already shows a simple picture of the part, the table tells you where to find it. For parts that no lesson shows on their own, the wiring is in this appendix (sections **A1–A10**), each with a short sketch to test it.

All pictures use the same layout as the lessons: two breadboards clipped together, ESP32 across the join, USB socket on the left. Pin numbers are the GPIO numbers the sketches use. Your board prints most of them with a **D** in front (pin 26 is **D26**), pins 16 and 17 as **RX2** and **TX2**, and the 5 V pin as **VIN**.

!!! warning "Two rules for every part"
    1. Wire with the USB cable **unplugged**. Plug it in when you've checked every wire.
    2. ESP32 pins work at **3.3 V**. A part powered from **5 V (VIN)** must never send 5 V back into a pin. Parts that need it (the ultrasonic sensor) get a resistor divider.

## Where to find each part

| Part | Wiring picture | Notes |
|---|---|---|
| ESP32 board + USB-C cable | Lesson 1, §4 | |
| Breadboards (2) | Lesson 1, §4 | Clip them together, ESP32 across the join |
| LED + 220 Ω resistor | Lesson 1, §4 | Long leg towards the pin |
| RGB LED | Lesson 5, §3 | Leave out the knob on 34 if you only want the LED |
| Push button | **A1** | |
| Tilt ball switch | **A2** | |
| Potentiometer (10 kΩ knob) | **A3** | |
| Photoresistor | **A4** | Needs a 10 kΩ resistor |
| Thermistor | **A5** | Needs a 10 kΩ resistor |
| Joystick module | **A6** | + goes to 3V3, not 5V |
| Active buzzer | Lesson 6, §2 | |
| Passive buzzer | Lesson 6, §2 | Same wiring as the active buzzer (+ leg to pin 33) |
| 1-digit 7-segment display | Lesson 7, §2 | The button on 13 is optional |
| 74HC595 shift register | Lesson 8, §3 | The 8 LEDs show its outputs; the knob is optional |
| 4-digit 7-segment display | Lesson 9, §2 | The button is optional |
| 0.96" OLED display | Lesson 10, §2 | |
| DHT11 temperature and humidity | **A7** | |
| GY-6500 motion sensor | **A8** | |
| Ultrasonic sensor HC-SR04 | Lesson 12, §2 | Needs the 1 kΩ / 2 kΩ divider on ECHO |
| PIR motion sensor HC-SR501 | Lesson 13, §2 | The green LED on 26 shows "motion" |
| Servo SG90 | Lesson 14, §3 | Power from VIN (5 V) |
| DC motor + fan blade | Lesson 15, §3 | Always through the L293D, never straight from a pin |
| L293D motor driver chip | Lesson 15, §3 | |
| Power supply module + 9V battery | Lesson 15, §3 | Set its jumpers to 5V; share GND with the ESP32 |
| Stepper motor + ULN2003 board | Lesson 15, §5 | Powered from the power supply module |
| 4×4 membrane keypad | Lesson 16, §2 | The buzzer is optional |
| RC522 RFID reader | Lesson 17, §2 | 3V3 only! |
| IR receiver module + remote | Lesson 18, §2 | |
| IR transmitter module | **A9** | |
| 5V relay | **A10** | Needs the transistor and the diode |
| NPN transistor PN2222 | **A10** | |
| Diode (rectifier) | **A10** | |
| Resistors | Lessons 1, 4, 12 and A10 | 220 Ω for LEDs, 10 kΩ for sensor dividers, 1 kΩ + 2 kΩ divider, 1 kΩ for a transistor |
| Jumper wires, female-to-male wires | | Female-to-male wires join modules (and the relay) to the breadboard |

## A1. Push button

A button joins its two sides when you press it. Wire one side to a pin and the other side to GND. The sketch turns on the pin's built-in **pull-up**, so the pin reads `HIGH` normally and `LOW` while you press.

| ✓ | From | To |
|---|---|---|
| [ ] | ESP32 **GND** | **–** rail |
| [ ] | Push button | across the middle gap |
| [ ] | ESP32 pin **13** | one leg of the button (jumper wire) |
| [ ] | diagonally opposite leg of the button | **–** rail |

@circuit A_button

@sketch A_Button

!!! tip "Always pressed, or never?"
    The button's legs come in joined pairs. If it never changes, turn it a quarter turn. Using the **diagonally opposite** legs always works.

## A2. Tilt ball switch

A tiny metal ball rolls inside the tube. Upright, it touches both legs and joins them. Tipped over, it rolls away. Wire it just like a button.

| ✓ | From | To |
|---|---|---|
| [ ] | ESP32 **GND** | **–** rail |
| [ ] | Tilt switch | across the middle gap (either way round) |
| [ ] | ESP32 pin **14** | one leg of the tilt switch (jumper wire) |
| [ ] | other leg | **–** rail |

@circuit A_tilt

@sketch A_Tilt

## A3. Potentiometer (knob)

The two outer legs go to 3V3 and GND. The middle leg slides between them, so pin **34** reads 0 at one end and 4095 at the other.

| ✓ | From | To |
|---|---|---|
| [ ] | ESP32 **GND** | **–** rail |
| [ ] | ESP32 **3V3** | **+** rail (the wire goes round the USB end) |
| [ ] | knob's left leg | **+** rail |
| [ ] | knob's right leg | **–** rail |
| [ ] | knob's middle leg | ESP32 pin **34** |

@circuit A_knob

**Test it:** upload **L04_ReadKnob** from Lesson 4 and open the Serial Plotter. Turn the knob. If it reads backwards, swap the two outer wires.

## A4. Photoresistor (light sensor)

A photoresistor's resistance drops when light falls on it. On its own the ESP32 can't measure resistance, so a **10 kΩ resistor** turns it into a voltage (a *divider*): brighter light means a bigger number on pin **35**.

| ✓ | From | To |
|---|---|---|
| [ ] | ESP32 **GND** | **–** rail |
| [ ] | ESP32 **3V3** | **+** rail (round the USB end) |
| [ ] | photoresistor | one leg in the **+** rail, the other in a free row |
| [ ] | 10 kΩ resistor (brown-black-orange) | from the same row to the **–** rail |
| [ ] | ESP32 pin **35** | the same row (jumper wire) |

@circuit A_light

@sketch A_Light

## A5. Thermistor

A thermistor is a resistor that changes with temperature: warmer means lower resistance. It needs a 10 kΩ divider too, the other way round from the photoresistor: the resistor goes to 3V3 and the thermistor to GND.

| ✓ | From | To |
|---|---|---|
| [ ] | ESP32 **GND** | **–** rail |
| [ ] | ESP32 **3V3** | **+** rail (round the USB end) |
| [ ] | 10 kΩ resistor (brown-black-orange) | one leg in the **+** rail, the other in a free row |
| [ ] | thermistor (small black bead) | from the same row to the **–** rail (either way round) |
| [ ] | ESP32 pin **34** | the same row (jumper wire) |

@circuit A_thermistor

@sketch A_Thermistor

!!! tip "Is it working?"
    Pinch the thermistor between your fingers. The temperature should climb within a few seconds. If it goes *down*, the resistor and thermistor are swapped.

## A6. Joystick module

The joystick is two knobs (left–right and up–down) plus a button you press by pushing the stick down. Use female-to-male wires.

| ✓ | Joystick pin | To |
|---|---|---|
| [ ] | **GND** | **–** rail (ESP32 GND joins it) |
| [ ] | **+5V** | **+** rail = ESP32 **3V3** (yes, **3V3**, not 5V!) |
| [ ] | **VRx** | ESP32 pin **34** |
| [ ] | **VRy** | ESP32 pin **35** |
| [ ] | **SW** | ESP32 pin **14** |

@circuit A_joystick

**Test it:** upload **L14_Joystick** from Lesson 14 and open the Serial Monitor.

!!! warning "Why 3V3?"
    At 5 V the joystick would send up to 5 V into pins 34 and 35. That is too much for the ESP32.

## A7. DHT11 temperature and humidity module

The blue DHT11 sends its readings down one wire. Use female-to-male wires.

| ✓ | DHT11 pin | To |
|---|---|---|
| [ ] | **–** | board B's **–** rail (ESP32 GND joins it) |
| [ ] | **+** | board B's **+** rail (ESP32 **3V3** joins it) |
| [ ] | **S** | ESP32 pin **4** |

@circuit A_dht11

**Test it:** install the **DHT sensor library** (see Lesson 11), then upload **L11_ReadDHT** from Lesson 11. Breathe on the sensor and watch the humidity rise.

## A8. GY-6500 motion sensor

The GY-6500 measures tilt and turning. It talks over **I²C**: two wires, **SDA** and **SCL**, that other I²C parts (like the OLED) can share. Only 4 of its 10 pins are needed. Plug it into board B and run four wires in a "staircase":

| ✓ | GY-6500 pin | To |
|---|---|---|
| [ ] | **VCC** | ESP32 **3V3** |
| [ ] | **GND** | ESP32 **GND** |
| [ ] | **SCL** | ESP32 pin **22** |
| [ ] | **SDA** | ESP32 pin **21** |

@circuit A_gy6500

**Test it:** upload **L19_Tilt** from Lesson 19 and open the Serial Plotter. Tilt the breadboard and watch x and y change.

## A9. IR transmitter module

The IR transmitter is a remote control's light: an LED that shines **infrared**, which your eyes can't see. Point it at a friend's ESP32 that has the IR receiver from Lesson 18.

| ✓ | IR transmitter pin | To |
|---|---|---|
| [ ] | **–** | board B's **–** rail (ESP32 GND joins it) |
| [ ] | **+** | board B's **+** rail (ESP32 **3V3** joins it) |
| [ ] | **S** | ESP32 pin **4** |

@circuit A_ir_tx

Install the **IRremote** library (see Lesson 18), then:

@sketch A_IRSend

!!! tip "Check the pin labels"
    Modules differ: read the letters printed next to the pins and match **S**, **+** and **–**, whatever order they come in.

!!! tip "Can't tell if it's on?"
    Look at the LED through a phone camera. Many cameras show infrared as a faint purple flicker.

## A10. Relay (with the transistor and the diode)

A **relay** is a switch worked by a magnet. Current through its **coil** pulls a metal arm across with a *click*, which joins the **COM** pin to the **NO** ("normally open") pin. The coil needs 5 V and about 70 mA, which is far more than an ESP32 pin can give. So the pin switches a **transistor**, and the transistor switches the coil. The **diode** soaks up the kick of voltage the coil gives when it switches off, so the transistor isn't damaged.

Here the relay switches a red LED, so you can see (and hear) it working.

!!! info "Meet the three new parts"
    - **PN2222 transistor:** hold it with the **flat face towards you**. The legs are **E** (emitter), **B** (base), **C** (collector), left to right.
    - **Diode:** current flows one way only. The **stripe** marks the **K** (cathode) end.
    - **Relay:** the pins are underneath. The two **coil** pins sit either side of **COM**. **NC** and **NO** are at the other end. The relay's top has a small picture of its pins.

| ✓ | From | To |
|---|---|---|
| [ ] | ESP32 **GND** | board A's **–** rail |
| [ ] | ESP32 **VIN** (5 V) | board A's **+** rail. *This rail is 5 V now!* |
| [ ] | PN2222 | three legs in three rows, flat face towards you |
| [ ] | ESP32 pin **32** | a free row on the other side of the gap (jumper wire) |
| [ ] | 1 kΩ resistor (brown-black-red) | from that row across the gap to the transistor's **B** row |
| [ ] | transistor's **E** row | **–** rail |
| [ ] | diode | from the transistor's **C** row to a free row; **stripe** away from the transistor |
| [ ] | the diode's stripe row | **+** rail (5 V) |
| [ ] | relay **coil** pin (C1) | **+** rail (5 V), female-to-male wire |
| [ ] | relay **coil** pin (C2) | transistor's **C** row, female-to-male wire |
| [ ] | relay **COM** | **+** rail (5 V), female-to-male wire |
| [ ] | relay **NO** | a free row, female-to-male wire |
| [ ] | 220 Ω resistor | from the NO row to a free row |
| [ ] | red LED | long leg in the resistor's row, short leg in the **–** rail |

@circuit A_relay

@sketch A_Relay

!!! warning "Check the diode before you plug in"
    The stripe must face the **5 V** side. Backwards, it joins 5 V to GND every time the transistor switches on.

!!! tip "LED on when the relay is off?"
    You found **NC** ("normally closed") instead of **NO**. Swap those two wires.

!!! warning "Small voltages only"
    In class, a relay only ever switches the kit's own 5 V or 9 V. Never connect it to a wall socket.
