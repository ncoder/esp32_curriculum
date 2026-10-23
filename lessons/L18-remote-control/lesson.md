---
lesson: 18
title: Remote Control
tagline: Use invisible infrared light to control your ESP32 from across the room.
learn:
  - How an **infrared (IR)** remote sends messages with flashes of light
  - How to **decode** remote buttons into code numbers
  - How to choose between many options with **switch / case**
  - How to make your own remote with the IR transmitter (challenge)
parts:
  - ESP32 board + USB-C cable, 2 breadboards
  - IR receiver module
  - Remote control (with its battery)
  - RGB LED
  - 3 resistors, 220 Ω (red-red-brown)
  - 3 female-to-male Dupont wires, jumper wires
  - "Challenge: IR transmitter module, 2 buttons"
plan:
  - {time: "0:00", do: "Invisible light: look through a phone camera"}
  - {time: "0:10", do: "Wire the IR receiver"}
  - {time: "0:20", do: "Sketch 1: **L18_ReadCodes** — map every button"}
  - {time: "0:50", do: "Short break"}
  - {time: "0:55", do: "Add the RGB LED"}
  - {time: "1:05", do: "Sketch 2: **L18_RemoteLights**"}
  - {time: "1:30", do: "Challenges"}
  - {time: "1:55", do: "Quiz and tidy up"}
---

## 1. Invisible light

A TV remote has a small LED on the front, but when you press a button you can't see it light up. That's because it gives off **infrared (IR)** light, a colour just past red that human eyes can't see.

!!! question "Try it: see the invisible"
    Point the remote at a phone camera (the front selfie camera often works best) and press a button. You'll see the LED flicker on the screen! Cameras can see a little infrared.

The remote doesn't just switch the light on. It **flashes it in a pattern** about 38,000 times a second, like super-fast Morse code. Each button has its own pattern. The receiver turns the pattern back into a number.

!!! info "Big idea: a protocol is an agreed language"
    The remote and receiver both follow the same rules, called a **protocol**. Our remote uses the **NEC** protocol: every button press sends an **address** (which device) and a **command** (which button).

## 2. Wire the IR receiver

The IR receiver module has 3 pins. Look closely at the labels. They are usually **–** (or G), **+** (or V, middle) and **S** (signal).

| ✓ | IR receiver pin | ESP32 pin |
|---|---|---|
| [ ] | **–** / G | **GND** |
| [ ] | **+** / V (middle) | **3V3** |
| [ ] | **S** / signal | **14** |

!!! tip "Install the library"
    **Tools → Manage Libraries…**, search **IRremote**, and install **IRremote by shirriff, z3t0, ArminJo**.

## 3. Sketch 1: What does each button say?

Type this in and save it as **L18_ReadCodes**. Upload it and open the **Serial Monitor** (115200 baud). Pull the plastic tab out of the remote's battery, point it at the receiver and press some buttons.

@sketch L18_ReadCodes

Fill in the code for each button. **Hold** a button down. What do you notice?

| Button | Code | Button | Code | Button | Code |
|---|---|---|---|---|---|
| POWER | 0x______ | 1 | 0x______ | 6 | 0x______ |
| VOL+ | 0x______ | 2 | 0x______ | 7 | 0x______ |
| VOL– | 0x______ | 3 | 0x______ | 8 | 0x______ |
| ▶‖ | 0x______ | 4 | 0x______ | 9 | 0x______ |
| UP | 0x______ | 5 | 0x______ | 0 | 0x______ |
| DOWN | 0x______ | EQ | 0x______ | ST/REPT | 0x______ |

### How it works

| Code | What it means |
|---|---|
| `#include <IRremote.hpp>` | Use the IRremote library (note: `.hpp`, not `.h`) |
| `IrReceiver.begin(IR_PIN);` | Start listening for IR on pin 14 |
| `if (IrReceiver.decode())` | **True** when a full message has arrived and been decoded |
| `IrReceiver.decodedIRData.command` | The button's command number |
| `Serial.println(code, HEX);` | Print the number in **hexadecimal**, like `45` instead of `69` |
| `0x45` | How we write a hex number in code. `0x45` = 69 |
| `IrReceiver.resume();` | "I'm done with that one, get ready for the next" |

!!! warning "Getting 0x0 or weird numbers?"
    Make sure the remote's battery tab is out. Bright sunlight or lamps can confuse the receiver. Point the remote straight at it, from less than 2 metres.

## 4. Add the RGB LED

| ✓ | From | To |
|---|---|---|
| [ ] | ESP32 pin **25** | 220 Ω resistor → RGB **red** leg |
| [ ] | ESP32 pin **26** | 220 Ω resistor → RGB **green** leg |
| [ ] | ESP32 pin **27** | 220 Ω resistor → RGB **blue** leg |
| [ ] | RGB **longest leg** (common –) | **–** rail |

## 5. Sketch 2: Remote control lights

Save as **L18_RemoteLights** and type this. If your codes in the table are different from the ones below, **use your codes**.

@sketch L18_RemoteLights

### How it works

| Code | What it means |
|---|---|
| `switch (code) { … }` | Look at `code` and jump to the matching `case` |
| `case 0x0C: … break;` | If `code` is `0x0C`, do this, then `break` out of the switch |
| *(no matching case)* | Nothing happens. Other buttons are ignored |
| `color(255, 120, 0);` | Our function from the PWM lesson: red, green, blue from 0 to 255 |

!!! tip "switch vs. lots of ifs"
    `switch` does the same job as `if (code == 0x0C) … else if (code == 0x18) …`, but is easier to read when there are many choices. Don't forget the `break`! Without it, the code "falls through" into the next case.

!!! question "Try it"
    1. Add buttons 6, 7, 8 and 9 with your own colours (purple, cyan, pink…).
    2. Does it work if you bounce the IR off a wall or the ceiling?
    3. Try your TV remote at home (or a friend's). Do its buttons give different codes?

## 6. Challenges

!!! challenge "Challenge 1: Brighter, dimmer"
    Make **VOL+** and **VOL–** change the brightness. *Hint: keep a `brightness` variable from 0 to 100, and use `r * brightness / 100` in `analogWrite`.*

!!! challenge "Challenge 2: Power toggle"
    Make **POWER** switch the light off **and** back on to the same colour. *Hint: a `bool isOn` and `isOn = !isOn;`*

!!! challenge "Challenge 3: Party mode"
    Button **0** starts random colours every 150 ms until another button is pressed. Use `random(256)`.

!!! challenge "Bonus: Build your own remote"
    The kit has an **IR transmitter** module too. With a friend, wire it to one ESP32 (signal on pin **4**, power to 3V3, GND to GND) plus two buttons on 13 and 14. Use `IrSender.begin(4);` and `IrSender.sendNEC(0x00, 0x0C, 0);` to send "button 1" to your friend's ESP32!

## 7. Quiz

!!! question "Check what you learned"
    1. Why can't you see the light from a remote control?
    @lines 1
    2. What does `break` do in a `switch`?
    @lines 1
    3. What number is `0x10` in normal (decimal) numbers? *(Hint: hex counts in sixteens)*
    @lines 1
    4. Name two things in your house that might use IR remotes.
    @lines 1

**Tidy up:** unplug the USB cable and **put the plastic tab back in the remote** (or take out the battery) so it doesn't run flat.
