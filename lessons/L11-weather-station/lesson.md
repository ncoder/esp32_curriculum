---
lesson: 11
title: Weather Station
tagline: Measure temperature and humidity and show them on your screen.
learn:
  - How a **sensor** turns the world into numbers
  - What **humidity** is
  - How to use **float** numbers with a decimal point
  - How to make decisions with **if / else if**
parts:
  - ESP32 board + USB-C cable, on your 2 breadboards
  - OLED screen, still wired from Lesson 10
  - DHT11 temperature and humidity module (blue, 3 pins)
  - 3 jumper wires
  - "*For a challenge:* thermistor + 10 kΩ resistor (brown-black-orange)"
plan:
  - {time: "0:00", do: "How do sensors work? Install the DHT library"}
  - {time: "0:15", do: "Wire up the DHT11"}
  - {time: "0:25", do: "Sketch 1: **L11_ReadDHT** (Serial Monitor)"}
  - {time: "0:50", do: "Short break"}
  - {time: "0:55", do: "Sketch 2: **L11_Station** (on the screen)"}
  - {time: "1:15", do: "Sketch 3: **L11_Comfort** (comfort face)"}
  - {time: "1:35", do: "Challenges"}
  - {time: "1:55", do: "Quiz and tidy up"}
---

## 1. Measuring the weather

A **sensor** is a part that measures something in the world and turns it into an electrical signal. Your microcontroller can then read it as a number.

The blue **DHT11** module has two sensors in one:

- a **thermometer** that measures **temperature** in degrees Celsius (°C)
- a **humidity** sensor that measures how much **water vapour** is in the air, in percent (%)

!!! info "Big idea: humidity"
    Air always holds some invisible water. 30% humidity feels dry (your lips get chapped). 80% feels damp and sticky, like a bathroom after a hot shower. Most people feel comfortable between about 30% and 60%.

The DHT11 has a tiny chip inside that does the measuring. It sends the answers to the ESP32 as a stream of 1s and 0s on **one wire**. Decoding that stream is tricky, so we use a library.

**Install the library:**

- [ ] **Tools → Manage Libraries…**
- [ ] Search for **DHT sensor library** (by Adafruit)
- [ ] Click **Install**, then **Install All** to get *Adafruit Unified Sensor* too.

## 2. Wire up the DHT11

Keep the OLED screen wired up from Lesson 10. Push the DHT11 module into the breadboard and **read the labels** on its pins. They are usually **S** (signal), **+** and **–**.

| ✓ | DHT11 pin | ESP32 pin |
|---|---|---|
| [ ] | **S** (signal / DATA / OUT) | **4** |
| [ ] | **+** (VCC) | **3V3** |
| [ ] | **–** (GND) | **GND** |

!!! warning "Check before you plug in"
    If + and – are swapped, the sensor gets hot and can be damaged. Double-check, then plug in the USB cable.

## 3. Sketch 1: Read the sensor

Type this in and save it as **L11_ReadDHT**. Open the **Serial Monitor** (115200 baud).

@sketch L11_ReadDHT

| Code | What it means |
|---|---|
| `#include <DHT.h>` | Use the DHT library |
| `DHT dht(4, DHT11);` | Make a sensor called **dht**, on pin 4, of type **DHT11** |
| `float temp` | A **float** is a number that can have a decimal point, like 23.5 |
| `dht.readTemperature()` | Ask the sensor for the temperature in °C |
| `isnan(temp)` | "Is Not A Number?" This is true if the reading failed |
| `return;` | Stop this turn of `loop()` early, then start again from the top |

!!! question "Try it: be a scientist"
    1. What temperature and humidity does your sensor show?
    @lines 1
    2. **Breathe** gently on the sensor for 5 seconds. What happens to the humidity? Why?
    @lines 1
    3. Hold the sensor between your fingers (not on the pins). How high does the temperature get?
    @lines 1

!!! tip "Serial Monitor says: Could not read the sensor?"
    Check the S wire is on pin **4**. Wait a few seconds after uploading, because the sensor is slow to wake up.

## 4. Sketch 2: Weather station

Now let's show the readings on the screen, so your weather station works without a computer.

!!! tip "No computer needed"
    Once it's uploaded, your sketch stays in the ESP32. Unplug it from the computer and power it from a USB phone charger. Now it's a real weather station you can put anywhere!

Save as **L11_Station**:

@sketch L11_Station

| Code | What it means |
|---|---|
| Two `#include` lines | One sketch can use **two libraries** at once |
| `display.print(temp, 1);` | Print with **1** number after the decimal point: 23.4 |
| `display.print(humidity, 0);` | Print with **no** decimal places: 45 |
| `if (…) { … } else { … }` | If the reading failed, show an error. **Otherwise** show the numbers |

## 5. Sketch 3: Comfort face

Let's make the weather station tell us **how the room feels**, with a smiley or a sad face.

Save as **L11_Comfort**:

@sketch L11_Comfort

| Code | What it means |
|---|---|
| `String message = "Just right!";` | A **String** variable holds text. We start by guessing "Just right!" |
| `if … else if … else if …` | Check one thing after another. Only the **first** true one happens |
| `message == "Just right!"` | `==` compares: is the message *exactly* "Just right!"? This is either true or false |
| `void drawFace(bool happy)` | A **bool** is just true or false. The function draws a smile for true and a frown for false |

!!! info "Big idea: the black circle trick"
    There's no "draw a smile" command! So we draw a white circle, then a **black** circle slightly higher on top of it. Only a thin crescent of white is left: a smile. For a frown, the black circle goes slightly **lower**.

!!! question "Try it"
    1. Breathe on the sensor until the face turns sad. What message do you get?
    2. Change the numbers so that 22 °C counts as "Too hot!". Can you make the face sad by holding the sensor?

## 6. Challenges

!!! challenge "Challenge 1: Fahrenheit"
    Show the temperature in °F as well. *Hint: `dht.readTemperature(true)` gives Fahrenheit.*

!!! challenge "Challenge 2: Record breaker"
    Remember the **lowest** and **highest** temperature since the ESP32 started, and show them on the screen. *Hint: start with `float lowest = 100;`.*

!!! challenge "Challenge 3: Warning light"
    Add a red LED (with a 220 Ω resistor) on pin **26** that switches on when it's "Too hot!".

!!! challenge "Bonus: Thermistor thermometer"
    A **thermistor** is a resistor that changes with temperature. Wire: **3V3 → 10 kΩ resistor → pin 34 → thermistor → GND**. Read it with `analogReadMilliVolts(34)` and watch the number change when you hold it. Ask your teacher for the formula to turn it into °C, and compare it with the DHT11!

## 7. Quiz

!!! question "Check what you learned"
    1. What two things does the DHT11 measure?
    @lines 1
    2. What is the difference between an `int` and a `float`?
    @lines 1
    3. Why did the humidity go up when you breathed on the sensor?
    @lines 1

**Tidy up:** unplug the USB cable and put the DHT11 back in the kit. You can leave the screen wired for later lessons.
