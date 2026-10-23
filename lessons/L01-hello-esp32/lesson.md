---
lesson: 1
title: Hello, ESP32!
tagline: Meet your microcontroller, make it talk, and blink your first light.
learn:
  - What a **microcontroller** is
  - How to upload a **sketch** from the Arduino IDE
  - How to use the **Serial Monitor** to see messages
  - How to build a circuit on a **breadboard**
parts:
  - ESP32 board + USB-C cable
  - 2 breadboards
  - 1 red LED
  - 1 resistor, 220 Ω (red-red-brown)
  - 2 jumper wires
plan:
  - {time: "0:00", do: "Kit tour: what's in the box?"}
  - {time: "0:15", do: "Set up the Arduino IDE"}
  - {time: "0:35", do: "Sketch 1: **L01_Hello** (talk to the computer)"}
  - {time: "0:55", do: "Short break"}
  - {time: "1:00", do: "Build the LED circuit"}
  - {time: "1:20", do: "Sketch 2: **L01_Blink**"}
  - {time: "1:35", do: "Challenges"}
  - {time: "1:55", do: "Quiz and tidy up"}
---

## 1. Meet the ESP32

The ESP32 is a **microcontroller**: a tiny computer on one chip. It has no screen or keyboard. Instead it has **pins**, the metal legs along both sides of the board. Your program can switch each pin **on** (3.3 volts) or **off** (0 volts), or **read** what is connected to it.

Microcontrollers are hidden inside microwaves, toys, washing machines, cars and game controllers. The ESP32 is a powerful one: it even has **Wi-Fi** and **Bluetooth** built in.

!!! info "Big idea: a program for a microcontroller is called a *sketch*"
    You write the sketch on the computer in the **Arduino IDE**. Then you **upload** it down the USB cable. The ESP32 remembers it, even after you unplug it, and runs it again every time it gets power.

Find these on your ESP32 board:

- [ ] The **USB-C socket**: power and data come in here
- [ ] The **EN** (or RST) button: restarts your program
- [ ] The **BOOT** button: you only need it if uploading gets stuck
- [ ] The pin labels. Look for **GND**, **3V3** and **26** (it may say **D26** or **IO26**)

## 2. Set up the Arduino IDE

Your teacher may have done some of these steps already. Tick each one when it's done.

- [ ] Open the **Arduino IDE** app (version 2).
- [ ] **File → Preferences**. In *Additional boards manager URLs* paste:
  `https://espressif.github.io/arduino-esp32/package_esp32_index.json`
- [ ] **Tools → Board → Boards Manager**. Search **esp32** and install **esp32 by Espressif Systems**.
- [ ] Plug in your ESP32 with the USB-C cable.
- [ ] **Tools → Board → esp32 → ESP32 Dev Module**
- [ ] **Tools → Port**: pick the one that appeared when you plugged in (e.g. `COM3` or `/dev/cu.usbserial-…`)

!!! tip "No port showing up?"
    Try a different USB cable. Some cables only carry power, not data. On Windows or Mac you may need the **CP210x driver** from silabs.com. Ask your teacher.

## 3. Sketch 1: Make the ESP32 talk

**File → New Sketch**. Delete everything in the new window and type in the code below exactly. Capital letters matter! `Serial` is not the same as `serial`.

Then **File → Save As…** and name it **L01_Hello**.

@sketch L01_Hello

Click the **Upload** button (the round arrow →). Wait until it says *Done uploading*. Then open **Tools → Serial Monitor** and set the speed in the bottom corner to **115200 baud**.

!!! tip "Upload stuck on *Connecting……*?"
    Hold down the **BOOT** button on the ESP32 until the upload starts, then let go.

### How it works

| Code | What it means |
|---|---|
| `void setup() { … }` | Runs **once** when the ESP32 starts |
| `void loop() { … }` | Runs **over and over forever** |
| `Serial.begin(115200);` | Start talking to the computer at 115200 "bits per second" |
| `Serial.println("…");` | Print a message, then start a new line |
| `int count = 0;` | Make a **variable**, a labelled box that holds a whole number |
| `count = count + 1;` | Take what's in the box, add 1, put it back |
| `delay(1000);` | Wait 1000 milliseconds (= 1 second) |

!!! question "Try it"
    1. Change `Sparky` to a name you choose for your ESP32. Upload again.
    2. Change `delay(1000)` to `delay(100)`. What happens?
    3. Press the **EN** button on the board. What happens to the count?

!!! warning "Red error message?"
    Read the line number in the error. The most common mistakes are a missing `;` at the end of a line, a missing `}` bracket, or a typo in capital letters.

## 4. Build your first circuit

A **breadboard** lets you connect parts without soldering. Inside, each short row of 5 holes is joined by a metal strip. The long lines along the edges (marked **+** and **–**) are the **power rails**.

!!! info "Getting your breadboards ready"
    Clip your two breadboards together side by side. Push the ESP32 in so that its left row of pins sits in one breadboard and its right row in the other. Press gently and evenly. Now every pin has free holes next to it.

An **LED** (light emitting diode) only lets electricity flow one way. The **long leg** is **+** and goes towards the pin. The **short leg** is **–** and goes towards GND. The **resistor** limits the current so the LED doesn't burn out.

| ✓ | From | To |
|---|---|---|
| [ ] | ESP32 pin **GND** | breadboard **–** rail (jumper wire) |
| [ ] | ESP32 pin **26** | one leg of the **220 Ω resistor** |
| [ ] | other leg of the resistor | **long leg** of the red LED |
| [ ] | **short leg** of the LED | **–** rail |

Electricity flows in a loop: out of pin 26 → through the resistor → through the LED → back into GND. No loop means no light!

## 5. Sketch 2: Blink!

**File → New Sketch**, type this in, and save it as **L01_Blink**. Upload it.

@sketch L01_Blink

| Code | What it means |
|---|---|
| `const int LED_PIN = 26;` | A **constant**: a name for the number 26 that never changes |
| `pinMode(LED_PIN, OUTPUT);` | Pin 26 will *send out* electricity |
| `digitalWrite(LED_PIN, HIGH);` | Switch the pin **on** (3.3 V) |
| `digitalWrite(LED_PIN, LOW);` | Switch the pin **off** (0 V) |
| `// LED on` | A **comment**. The ESP32 ignores everything after `//` |

!!! tip "LED not lighting?"
    Turn the LED around: the long leg must go to the resistor. Check the GND wire is in the **–** rail. Check you used pin **26**.

## 6. Challenges

!!! challenge "Challenge 1: Speed it up"
    Make the LED blink really fast, then really slowly. What is the fastest blink your eyes can still see?

!!! challenge "Challenge 2: Heartbeat"
    Make the LED go *blink-blink……pause, blink-blink……pause* like a heartbeat.

!!! challenge "Challenge 3: SOS"
    In Morse code, SOS is **· · · – – – · · ·** (3 short, 3 long, 3 short). Make your LED flash SOS. *Hint: a short flash could be 200 ms and a long flash 600 ms.*

!!! challenge "Bonus: Blink and talk"
    Combine both sketches. Print `"ON"` and `"OFF"` in the Serial Monitor every time the LED changes.

## 7. Quiz

!!! question "Check what you learned"
    1. What is the difference between `setup()` and `loop()`?
    @lines 2
    2. Which leg of an LED is the **+** leg?
    @lines 1
    3. How many milliseconds are in 3 seconds?
    @lines 1

**Tidy up:** unplug the USB cable. You can leave your LED circuit on the breadboard for next time.
