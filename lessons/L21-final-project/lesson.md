---
lesson: 21
title: My Invention
tagline: Plan, build, test and show off a project of your own design.
learn:
  - How real engineers go from an **idea** to a working **prototype**
  - How to combine **inputs** and **outputs** from earlier lessons
  - How to build and test **one piece at a time**
  - How to explain your invention to others
parts:
  - ESP32 board + USB-C cable, 2 breadboards
  - Whatever your project needs (see your plan!)
  - "For the example: DHT11, PIR sensor, OLED, passive buzzer"
  - Your old sketches from lessons 1–20
  - A pencil
plan:
  - {time: "0:00", do: "The inventor's process + idea menu"}
  - {time: "0:15", do: "Example: the Smart Room Monitor"}
  - {time: "0:30", do: "Fill in your planning sheet"}
  - {time: "0:50", do: "Short break"}
  - {time: "0:55", do: "Build and test, one piece at a time"}
  - {time: "1:40", do: "Show and tell"}
  - {time: "1:55", do: "Reflection and tidy up"}
---

## 1. You are the inventor now

You've learned about LEDs, buttons, sounds, screens, sensors, motors, cards, remotes and Wi-Fi. Today **you** decide what to build!

!!! info "Big idea: the inventor's loop"
    Real engineers don't build everything at once. They follow a loop:
    **Idea → Plan → Build a small piece → Test → Fix → Build the next piece…** and finally **Show**.
    If something goes wrong, that's normal. It's just the *Test → Fix* part of the loop.

Every invention is made of **inputs** (things that sense the world) and **outputs** (things that do something):

| Inputs (sense) | Outputs (do) |
|---|---|
| Button, keypad, knob, joystick, tilt switch | LED, RGB LED, 7-segment display |
| Light sensor, temperature (DHT11), thermistor | Buzzer: beeps and tunes |
| Distance (ultrasonic), motion (PIR), tilt (GY-6500) | OLED screen: words, numbers, pictures |
| RFID card, IR remote, Wi-Fi web page | Servo, stepper motor, fan motor |

## 2. Idea menu

Pick one, change one, or invent your own!

| Idea | What it does | Main parts | Lessons to look back at |
|---|---|---|---|
| **Smart Room Monitor** | Shows temperature, warns when too hot, chimes when someone comes in | DHT11, PIR, OLED, buzzer | 10, 11, 13 |
| **Secret Treasure Box** | Opens a servo lock with the right card *or* keypad code | RFID or keypad, servo, LEDs | 14, 16, 17 |
| **Parking Helper** | Beeps faster and shows distance as a car gets closer | Ultrasonic, buzzer, OLED or LEDs | 6, 10, 12 |
| **Reaction Game** | Two players race to press their button after a light | Buttons, LEDs, 4-digit display | 3, 9 |
| **Plant Guardian** | Warns when it's too dark or too hot for a plant | Photoresistor, DHT11, RGB LED | 4, 5, 11 |
| **Desk Fan Controller** | Fan speeds up when it's warmer; remote to turn it off | DHT11, DC motor, IR remote | 11, 15, 18 |
| **Phone-Controlled Disco** | Pick colours and tunes from a web page | RGB LED, buzzer, Wi-Fi | 5, 6, 20 |
| **Intruder Alarm** | Arm with a keypad code; motion sets off a siren | PIR, keypad, buzzer, LEDs | 13, 16 |

## 3. Worked example: Smart Room Monitor

Here is one finished project, so you can see how the pieces come together. You can build it as it is, or use it as a starting point and change it.

| ✓ | Part | Pin | Power |
|---|---|---|---|
| [ ] | DHT11 **S** (signal) | **4** | + to **3V3**, – to **GND** |
| [ ] | PIR **OUT** (middle) | **27** | VCC to **5V**, GND to **GND** |
| [ ] | Buzzer **+** | **33** | – to **GND** |
| [ ] | OLED **SDA / SCL** | **21 / 22** | VCC to **3V3**, GND to **GND** |

@sketch L21_SmartRoom

### Where did each piece come from?

| Part of the sketch | Learned in |
|---|---|
| `DHT dht(DHT_PIN, DHT11);` and `readTemperature()` | Lesson 11: Weather Station |
| `if (millis() - lastRead > 2000)` (do something every 2 s without `delay`) | Lesson 9 |
| `digitalRead(PIR_PIN)` and remembering `wasMotion` | Lesson 13: Motion Alarm |
| `if (motion && !wasMotion)`: only beep at the **moment** motion starts | Lesson 3 (buttons) |
| `display.print(temp, 1)`: show 1 decimal place | Lesson 10: OLED |

!!! tip "Notice the comments"
    The `loop()` is split into steps: **1. read**, **2. decide**, **3. show**. Most inventions follow this pattern. It's a great way to plan your own sketch!

## 4. My planning sheet

**My invention is called:**

@lines 1

**What it does (one or two sentences):**

@lines 2

**Who would use it, and why?**

@lines 1

**Inputs and outputs:**

<table style="width:100%"><tr><th>Inputs (what it senses)</th><th>Outputs (what it does)</th></tr><tr style="height:30px"><td>&nbsp;</td><td>&nbsp;</td></tr><tr style="height:30px"><td>&nbsp;</td><td>&nbsp;</td></tr><tr style="height:30px"><td>&nbsp;</td><td>&nbsp;</td></tr></table>

**Parts list and pins:**

<table style="width:100%"><tr><th>✓</th><th>Part</th><th>ESP32 pin(s)</th><th>Power (3V3 or 5V)</th><th>Lesson to look back at</th></tr><tr style="height:30px"><td>[ ]</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr style="height:30px"><td>[ ]</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr style="height:30px"><td>[ ]</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr style="height:30px"><td>[ ]</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr style="height:30px"><td>[ ]</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table>

!!! warning "Pin check before you wire"
    Use pins from your earlier lessons. **Don't use** pins 0, 2, 12 or 15. Pins 34–39 are **input only**. Two parts can't share one pin, except I²C parts (OLED and GY-6500) on 21/22. 5 V parts like the servo and ultrasonic sensor get power from **5V**, but the ESP32 pins only take 3.3 V!

**Sketch plan: what will `loop()` do?** Write it in plain words first.

<table style="width:100%"><tr><th>Step</th><th>What my sketch does</th></tr><tr style="height:30px"><td>1. <b>Read</b> the inputs</td><td>&nbsp;</td></tr><tr style="height:30px"><td>2. <b>Decide</b> what to do</td><td>&nbsp;</td></tr><tr style="height:30px"><td>3. <b>Show / do</b> something</td><td>&nbsp;</td></tr></table>

## 5. Build and test, one piece at a time

!!! info "The golden rule"
    **Never wire everything and write everything at once.** Add **one** part, get it working, then add the next. When something breaks, you'll know it was the last thing you added.

- [ ] Step 1: wire your **first input** and print its value to the Serial Monitor
- [ ] Step 2: wire your **first output** and test it on its own
- [ ] Step 3: connect them with an `if`: *when input does X, output does Y*
- [ ] Step 4: add the next part… and test again
- [ ] Step 5: make it fun: sounds, messages, animations

**Test log:** write down what you tried, especially when it didn't work!

<table style="width:100%"><tr><th>What I tried</th><th>What happened</th><th>What I'll change</th></tr><tr style="height:30px"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr style="height:30px"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr style="height:30px"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr style="height:30px"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table>

!!! tip "Stuck?"
    1. Open the sketch from the lesson that used the part, and check the wiring and code against it.
    2. Add `Serial.println(…)` to see what your variables really are.
    3. Explain your code out loud to a friend (or a rubber duck!). You'll often spot the problem yourself.

## 6. Show and tell

Each inventor gets **2 minutes**. Use these prompts:

- [ ] What is it called and what problem does it solve?
- [ ] Demo: show it working!
- [ ] What was the hardest bug, and how did you fix it?
- [ ] What would you add if you had another 2 hours?

!!! challenge "Extension: level it up"
    Finished early? Add a **Wi-Fi web page** (Lesson 20) so your invention can be checked or controlled from a phone. Your teacher has an example that adds this to the Smart Room Monitor.

## 7. Reflection

!!! question "Look back"
    1. Which lesson was your favourite, and why?
    @lines 1
    2. What's one thing you can do now that you couldn't do in Lesson 1?
    @lines 1
    3. Name one invention you'd love to build next, maybe with parts that aren't in the kit.
    @lines 2

**Tidy up:** take a photo of your project! Then carefully put every part back in its place in the kit. Congratulations, inventor! 🎉
