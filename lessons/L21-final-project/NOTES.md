# Lesson 21 teacher notes

**Format:** this is an open project session. Two hours is enough for a
small project; many groups will want more. If you can, run it over **two
sessions**: plan + first build in session 1, finish + show and tell in
session 2. The planning sheet in the handout then carries over.

**Before class:** remind students to bring (or have on the computer) their
sketches from earlier lessons; they're the best reference. Have spare parts
ready for popular ideas: extra buttons, LEDs and Dupont wires.

**Steering project choices:**

- Encourage **2–3 parts**, not 6. A finished small project beats an
  unfinished big one. Ambitious students can add parts after the core works.
- Check the planning sheet's pin table before they wire. Watch for: two
  parts on the same pin; buttons on input-only pins 34–39 (no pull-up);
  5 V to an ESP32 pin (ultrasonic ECHO needs the divider); servo + RFID
  both on 18 (move the servo to 13).
- Motors (DC fan, stepper) need the power supply module. Budget time for it.

**The example sketch** (`L21_SmartRoom`) is optional to type. Some students
like to start from it and modify it; others start from their own plan. It
shows the "read → decide → show" structure and edge detection
(`motion && !wasMotion`) which most projects need.

**Common problems**

- *Everything was working until I added X:* the golden rule. Remove X,
  check, re-add it.
- *DHT11 shows `nan`:* reading too often or the wrong pin. The extension
  solution shows how to ignore failed readings with `isnan()`.
- *OLED and something else both stopped:* I²C wiring disturbed while
  adding parts; reseat SDA/SCL.
- *Board resets when the motor/servo moves:* power. Use the power supply
  module, and share GND.

**Assessment ideas:** the planning sheet, test log and the 2-minute
show-and-tell give a good picture of understanding. Reward good debugging
stories as much as finished projects.

**Extension solution:** `solutions/L21_SmartRoomPlus` adds a visitor
counter, an automatic "fan" LED on pin 26 when too hot, and a Wi-Fi page at
192.168.4.1 (network `SmartRoom-ESP32`, password `smartroom1`).
