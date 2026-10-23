---
lesson: 2
title: Traffic Lights
tagline: Control three LEDs, make them take turns, and write your own function.
learn:
  - How to control **several pins** at once
  - How to plan a **sequence** of steps
  - How to write your own **function**
  - How an **array** and a **for loop** save typing
parts:
  - ESP32 board + USB-C cable
  - 2 breadboards
  - 1 red, 1 yellow and 1 green LED
  - 3 resistors, 220 Ω (red-red-brown)
  - 4 jumper wires
plan:
  - {time: "0:00", do: "Warm-up: how does a real traffic light work?"}
  - {time: "0:10", do: "Build the three-LED circuit"}
  - {time: "0:30", do: "Sketch 1: **L02_TrafficLight**"}
  - {time: "0:55", do: "Short break"}
  - {time: "1:00", do: "Sketch 2: **L02_LightFunction** (your own function)"}
  - {time: "1:20", do: "Sketch 3: **L02_Chase** (arrays and for loops)"}
  - {time: "1:35", do: "Challenges"}
  - {time: "1:55", do: "Quiz and tidy up"}
---

## 1. Warm-up: think like a traffic engineer

A traffic light is a little computer that follows a **sequence**: the same steps, in the same order, forever. Before you write any code, write down the steps. Number them, and say which lights are on and for how long.

!!! question "Plan your traffic light"
    Write each step: which colours are on, and how many seconds it lasts.
    @lines 3

In this lesson we will use **red → green → yellow → back to red**. Some countries do it differently. You'll get to change it in a challenge.

## 2. Build the circuit

This is the same idea as the LED from Lesson 1, done three times. Each LED gets its own pin and its own resistor. All three short legs share the **–** rail.

| ✓ | From | To |
|---|---|---|
| [ ] | ESP32 pin **GND** | breadboard **–** rail |
| [ ] | ESP32 pin **25** | 220 Ω resistor → **long leg** of the **red** LED |
| [ ] | ESP32 pin **26** | 220 Ω resistor → **long leg** of the **yellow** LED |
| [ ] | ESP32 pin **27** | 220 Ω resistor → **long leg** of the **green** LED |
| [ ] | **short legs** of all 3 LEDs | **–** rail |

!!! tip "Keep it tidy"
    Put the LEDs in a line, red at the top, like a real traffic light. Leave a gap between them so the legs don't touch.

## 3. Sketch 1: A traffic light

**File → New Sketch**, type this in, and save it as **L02_TrafficLight**. Upload it.

@sketch L02_TrafficLight

### How it works

| Code | What it means |
|---|---|
| `const int RED = 25;` | Give pin 25 a name we can remember |
| `pinMode(RED, OUTPUT);` | Each LED pin needs its own `pinMode` |
| three `digitalWrite` lines | Set **every** light for this step, even the ones that stay off |
| `delay(3000);` | Hold this step for 3 seconds |

!!! info "Big idea: the computer does exactly what you say"
    Why do we switch off lights that are already off? Because each step should say *exactly* what the light looks like. Then you can change the order of the steps and nothing goes wrong.

!!! question "Try it"
    1. Make the green light last twice as long.
    2. Add a fourth step: all three lights off for half a second.

## 4. Sketch 2: Write your own function

Sketch 1 has lots of lines that look almost the same. Programmers hate typing the same thing again and again! A **function** is a set of instructions with a name. We'll make one called `lights` that sets all three LEDs and then waits.

**File → Save As…** and name it **L02_LightFunction**. Then change your code to this:

@sketch L02_LightFunction

| Code | What it means |
|---|---|
| `void lights(int r, int y, int g, int wait)` | Make a function called `lights`. It needs 4 numbers, called **parameters** |
| `digitalWrite(RED, r);` | Use whatever was passed in as `r` (`HIGH` or `LOW`) |
| `lights(HIGH, LOW, LOW, 3000);` | **Call** the function: red on, yellow off, green off, wait 3 s |
| `void` | This function does something but doesn't give back an answer |

The light works exactly the same as before, but `loop()` is now 3 lines long and easy to read.

!!! tip "Same order every time"
    The values go into the parameters **in order**. In `lights(LOW, HIGH, LOW, 1000)` the first value goes to `r`, the second to `y`, the third to `g`, and the last to `wait`.

## 5. Sketch 3: Light chase

Now we'll stop being a traffic light and make a running light, like on a game show. **File → New Sketch**, save it as **L02_Chase**.

@sketch L02_Chase

| Code | What it means |
|---|---|
| `int leds[] = {25, 26, 27};` | An **array**: one name holding a list of numbers |
| `leds[0]` | The **first** item in the list (25). Counting starts at **0**! |
| `for (int i = 0; i < 3; i++)` | Repeat the `{ }` block with `i` = 0, then 1, then 2 |
| `i++` | Add 1 to `i` |

!!! info "Big idea: loops do the boring work"
    The `for` loop in `setup()` runs `pinMode` three times for you. With 30 LEDs you would only change the `3` and the array, not write 30 lines.

!!! question "Try it"
    1. Change `speed` to `50`. Then `500`.
    2. Delete the line `digitalWrite(leds[i], LOW);`. What happens? Why?

## 6. Challenges

!!! challenge "Challenge 1: UK traffic light"
    In the UK, red and yellow come on **together** before green. Change **L02_LightFunction** to do red → red + yellow → green → yellow.

!!! challenge "Challenge 2: Night mode"
    At night some traffic lights just flash yellow. Make a sketch that flashes the yellow light on and off, with the others off.

!!! challenge "Challenge 3: Bouncing light"
    Change **L02_Chase** so the light goes 25 → 26 → 27 → 26 → 25 → … and bounces back and forth. *Hint: add a second `for` loop that counts down with `i--`.*

!!! challenge "Bonus: All together now"
    Make all three LEDs blink together 3 times, then do one chase, then repeat. Write a function for each pattern.

## 7. Quiz

!!! question "Check what you learned"
    1. What is a **function**, and why is it useful?
    @lines 2
    2. In `int leds[] = {25, 26, 27};` what is `leds[2]`?
    @lines 1
    3. How many times does `for (int i = 0; i < 5; i++)` repeat?
    @lines 1

**Tidy up:** unplug the USB cable. Keep your three LEDs on the breadboard: you'll use them again in Lesson 3.
