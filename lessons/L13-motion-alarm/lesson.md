---
lesson: 13
title: Intruder Alert!
tagline: Build a motion-sensing burglar alarm that you can arm and disarm.
learn:
  - How a **PIR sensor** feels the heat of moving bodies
  - How to spot the moment something **changes** (an *edge*)
  - How to use a `bool` variable to remember if the alarm is **armed**
  - How to tune a sensor with its adjustment knobs
parts:
  - ESP32 board + USB-C cable
  - 2 breadboards
  - PIR motion sensor (HC-SR501, white dome)
  - 1 red LED and 1 green LED
  - 2 resistors, 220 Ω (red-red-brown)
  - 1 push button
  - Passive buzzer
  - Jumper wires (3 female-to-male for the PIR)
plan:
  - {time: "0:00", do: "How do motion sensors work?"}
  - {time: "0:10", do: "Wire up the PIR sensor and LED"}
  - {time: "0:25", do: "Sketch 1: **L13_Motion** (+ 1 minute warm-up)"}
  - {time: "0:40", do: "Knob experiments: range and timer"}
  - {time: "0:55", do: "Short break"}
  - {time: "1:00", do: "Add LEDs, button and buzzer"}
  - {time: "1:15", do: "Sketch 2: **L13_Alarm**"}
  - {time: "1:35", do: "Challenges: test your alarm on a friend!"}
  - {time: "1:55", do: "Quiz and tidy up"}
---

## 1. How does it see you?

Everything warm gives off invisible **infrared** light. People, cats and dogs glow brightly in infrared; walls and tables are dim. The **PIR** (Passive InfraRed) sensor has a heat-sensitive chip under its white dome.

The dome is a clever lens made of lots of little windows. When you walk past, your warm body moves from one window to the next, and the sensor notices the *change*. That is why it spots **moving** people but not a person who sits perfectly still.

!!! info "Big idea: the sensor does the hard work"
    The PIR sensor has its own little chip. It sends the ESP32 one simple signal: pin **HIGH** = *"I saw movement!"*, pin **LOW** = *"all quiet"*. Our code just has to read one pin.

## 2. Build the motion detector

Take the PIR sensor and carefully lift off the white dome to have a look (then put it back!). Find the 3 pins and their labels: **VCC**, **OUT**, **GND**.

Turn the sensor over. You'll find **two orange knobs** (use a small screwdriver or your fingernail):

- One is **SENSITIVITY**: how far away it can see (about 3 to 7 metres).
- One is **TIME**: how long OUT stays HIGH after it sees you (about 3 seconds to 5 minutes!).

Some boards have a little **jumper** too. If yours does, put it on **H** ("repeat"), so the timer keeps restarting while you keep moving.

| ✓ | From | To |
|---|---|---|
| [ ] | ESP32 **GND** | breadboard **–** rail |
| [ ] | ESP32 **5V** (may say **VIN**) | breadboard **+** rail |
| [ ] | PIR **VCC** | **+** rail (5 V) |
| [ ] | PIR **GND** | **–** rail |
| [ ] | PIR **OUT** | ESP32 pin **27** |
| [ ] | ESP32 pin **26** | 220 Ω resistor → **long leg** of the **green** LED |
| [ ] | short leg of the green LED | **–** rail |

!!! tip "The PIR is happy with 5 V"
    It needs 5 V to power itself, but its **OUT** pin only ever sends 3.3 V. So it is safe to connect straight to the ESP32, with no divider needed.

## 3. Sketch 1: Motion detector

!!! warning "Wait one minute!"
    When it first gets power, the PIR sensor needs about **1 minute** to learn what the room looks like. During this time it may trigger randomly. Keep still and be patient!

**File → New Sketch**, type this in, save it as **L13_Motion**, upload, and open the **Serial Monitor**.

@sketch L13_Motion

### How it works

| Code | What it means |
|---|---|
| `bool wasMoving = false;` | A `bool` holds only **true** or **false**. This one remembers what we saw *last time* |
| `digitalRead(PIR_PIN) == HIGH` | Is the sensor saying "movement"? The answer (true/false) goes in `moving` |
| `digitalWrite(LED_PIN, moving);` | `true` works like HIGH and `false` like LOW, so the LED copies the sensor |
| `moving && !wasMoving` | `&&` means **AND**, `!` means **NOT**. *Moving now* AND *not moving before* = it **just started** |
| `wasMoving = moving;` | Remember this reading for the next time round the loop |

!!! info "Big idea: catching the *edge*"
    The sensor stays HIGH for a few seconds. If we added 1 to `count` *every time* we saw HIGH, it would count hundreds per wave! Instead, we only count at the **edge**: the moment it changes from LOW to HIGH.

## 4. Tune your sensor

Remember the two orange knobs underneath the sensor? Now that your sketch is running, find out which knob is which.

!!! question "Detective work"
    1. Turn **one** knob fully anticlockwise. Wave, then stand still. How long does the LED stay on? Which knob did you turn?
    @lines 1
    2. Set the TIME knob to its **shortest** setting (you'll need it short for the alarm). How far across the room can the sensor see you?
    @lines 1
    3. After the LED goes off, the sensor ignores you for about 3 seconds. Can you find this "blind" moment?
    @lines 1

## 5. Sketch 2: Burglar alarm

Now let's make a real alarm. The **button** arms and disarms it. **Green** = disarmed (safe), **red** = armed. If someone moves while it's armed, the siren wails!

Add these parts:

| ✓ | From | To |
|---|---|---|
| [ ] | ESP32 pin **25** | 220 Ω resistor → **long leg** of the **red** LED |
| [ ] | short leg of the red LED | **–** rail |
| [ ] | ESP32 pin **13** | one leg of the **button** |
| [ ] | the button's **opposite** leg | **–** rail |
| [ ] | Buzzer **+** | ESP32 pin **33** |
| [ ] | Buzzer **–** | **–** rail |

**File → New Sketch**, type this in and save it as **L13_Alarm**.

@sketch L13_Alarm

| Code | What it means |
|---|---|
| `armed = !armed;` | Flip it: true becomes false, false becomes true |
| `digitalWrite(GREEN_PIN, !armed);` | Green is on when the alarm is **not** armed |
| `void siren() { … }` | Our own function: flash red and switch between two notes, 6 times |
| `while (digitalRead(BUTTON_PIN) == LOW)` | Keep waiting **while** the button is still held down |
| `armed && moving && !wasMoving` | Armed, AND moving now, AND not moving before |

!!! tip "The alarm goes off as soon as I arm it!"
    You're too close and moving! Arm it, then **freeze** until the PIR's timer runs out. Or point the sensor away from you. (Challenge 2 fixes this properly.)

## 6. Challenges

!!! challenge "Challenge 1: Silent alarm"
    Make a "spy mode" where the alarm only flashes the red LED and prints a message, with no sound, so the intruder doesn't know they've been spotted.

!!! challenge "Challenge 2: Exit delay"
    Real alarms give you time to leave. After arming, beep once a second for 10 seconds before the alarm becomes active. *Hint: a `for` loop with `tone()` and `delay(1000)`.*

!!! challenge "Challenge 3: Alarm diary"
    When the alarm goes off, print how long after arming it happened, like `Alarm 2 at 01:35`. *Hint: save `millis()` when you arm it, then subtract.*

!!! challenge "Bonus: Test it on a friend"
    Hide your alarm guarding a "treasure". Can a friend sneak up and grab it without setting it off? What tricks work against a PIR sensor?

## 7. Quiz

!!! question "Check what you learned"
    1. Why does the PIR see a walking person but not a statue of a person?
    @lines 2
    2. What does `!` mean in code? What is `!true`?
    @lines 1
    3. Why do we count motion only when `moving && !wasMoving`?
    @lines 2

**Tidy up:** unplug the USB cable. Put the PIR sensor's dome back on if you took it off.
