---
lesson: 17
title: Secret Agent Cards
tagline: Use RFID to read a card without touching it, and build an access-control door.
learn:
  - How **RFID** works (radio + a tiny chip with no battery)
  - How to read a card's unique ID, called its **UID**
  - How to compare **Strings** and search an **array** of allowed cards
  - How to build an access system with lights, sound and (bonus) a servo lock
parts:
  - ESP32 board + USB-C cable, 2 breadboards
  - RC522 RFID module + white card + blue key tag
  - 1 red LED, 1 green LED
  - 2 resistors, 220 Ω (red-red-brown)
  - Passive buzzer
  - 7 female-to-male Dupont wires, jumper wires
  - "Extension: SG90 servo"
plan:
  - {time: "0:00", do: "How does a bus pass work? RFID explained"}
  - {time: "0:15", do: "Wire up the RC522 reader"}
  - {time: "0:35", do: "Sketch 1: **L17_ReadCard** — find your card's UID"}
  - {time: "0:55", do: "Short break"}
  - {time: "1:00", do: "Add the LEDs and buzzer"}
  - {time: "1:10", do: "Sketch 2: **L17_Access** — allowed or denied?"}
  - {time: "1:35", do: "Challenges (servo door!)"}
  - {time: "1:55", do: "Quiz and tidy up"}
---

## 1. What is RFID?

**RFID** stands for **R**adio **F**requency **ID**entification. It's inside bus passes, library books, hotel key cards and pet microchips.

The reader has a coil of wire (an **antenna**) that sends out a radio wave. The card also has a coil and a tiny chip, but **no battery**. When the card comes close, the radio wave makes enough electricity in its coil to wake the chip up. The chip then whispers back its number.

!!! info "Big idea: every card has a UID"
    Each card has a **UID** (Unique IDentifier), a number set at the factory. Your card's UID is different from your neighbour's. Our program will decide who is allowed in by checking that number.

The UID is written in **hexadecimal** ("hex"), which counts using 16 symbols: `0 1 2 3 4 5 6 7 8 9 A B C D E F`. So a UID looks like `A3 4F 12 9B`.

## 2. Wire up the reader

!!! warning "3.3 V only!"
    The RC522 is a **3.3 V** part. Connect its power pin to **3V3**, never to 5V or VIN. 5 V can destroy it.

The RC522 talks to the ESP32 using **SPI**, a fast way of sending data over 4 wires. The ESP32 has special SPI pins, so use exactly these. Use female-to-male Dupont wires from the module's pins to the breadboard.

| ✓ | RC522 pin | ESP32 pin |
|---|---|---|
| [ ] | **3.3V** | **3V3** |
| [ ] | **GND** | **GND** |
| [ ] | **RST** | **4** |
| [ ] | **SDA** (also called SS) | **5** |
| [ ] | **SCK** | **18** |
| [ ] | **MISO** | **19** |
| [ ] | **MOSI** | **23** |
| [ ] | **IRQ** | *not connected* |

!!! tip "Install the library"
    **Tools → Manage Libraries…**, search **MFRC522**, and install **MFRC522 by GithubCommunity**.

## 3. Sketch 1: Read your card

Type this in and save it as **L17_ReadCard**. Upload it, open the **Serial Monitor** (115200 baud) and hold the card flat on the reader.

@sketch L17_ReadCard

Write down the UIDs of your card and your key tag. You'll need them next!

<table style="width:100%"><tr><th style="width:25%">Card</th><th>UID</th></tr><tr style="height:30px"><td>White card</td><td>&nbsp;</td></tr><tr style="height:30px"><td>Blue key tag</td><td>&nbsp;</td></tr></table>

### How it works

| Code | What it means |
|---|---|
| `MFRC522 rfid(SS_PIN, RST_PIN);` | Make a reader object called `rfid` |
| `SPI.begin();` `rfid.PCD_Init();` | Start SPI, then start the reader |
| `if (!rfid.PICC_IsNewCardPresent()) return;` | No card? Then `return`: stop this loop and start again. `!` means **not** |
| `rfid.uid.uidByte[i]` | Byte number `i` of the UID (an array of numbers) |
| `String(…, HEX)` | Turn a number into hex text, like `9b` |
| `uid += " ";` | Stick more text onto the end of the String |
| `uid.toUpperCase();` | `9b` becomes `9B` |
| `rfid.PICC_HaltA();` | Tell the card "thanks, go to sleep" so it's only read once |

!!! question "Try it"
    1. How far away can you hold the card and still read it?
    2. Does it work through your hand? Through a book? Through a metal tin lid?
    3. Try a bank card or a bus pass (only reading, it's safe). Do they have UIDs too?

## 4. Add lights and sound

Keep the reader connected and add:

| ✓ | From | To |
|---|---|---|
| [ ] | ESP32 pin **25** | 220 Ω resistor → **long leg** of the **red** LED |
| [ ] | ESP32 pin **27** | 220 Ω resistor → **long leg** of the **green** LED |
| [ ] | both LED **short legs** | **–** rail |
| [ ] | ESP32 pin **33** | passive buzzer **+** |
| [ ] | buzzer **–** | **–** rail |

## 5. Sketch 2: Access control

Save your first sketch as **L17_Access** and change it to this. **Replace the two UIDs** on the `allowed` line with the ones you wrote down. Keep the quotes and the spaces exactly.

@sketch L17_Access

### How it works

| Code | What it means |
|---|---|
| `String allowed[] = {"…", "…"};` | An **array of Strings**: the list of cards that may enter |
| `bool isAllowed(String uid)` | A function that answers **true** or **false** |
| `if (uid == allowed[i]) return true;` | `==` compares two Strings. Found it? Answer true straight away |
| `return false;` | Checked the whole list and no match: answer false |
| `tone(BUZZER_PIN, 1500, 150);` | High beep for 150 ms. A low 200 Hz buzz sounds like "nope!" |

!!! tip "Every card says denied?"
    Print the UID and compare it letter by letter with your list. Look for `0` vs `O`, missing spaces, or lowercase letters.

## 6. Challenges

!!! challenge "Challenge 1: Add a friend"
    Add a third card (borrow a friend's) to the list. Remember to change `NUM_ALLOWED` too!

!!! challenge "Challenge 2: Say hello"
    Make a second array `names[]` with a name for each card, and print `Welcome, Sam!` with the right name.

!!! challenge "Challenge 3: Servo door"
    Add a servo as a door lock: it turns to 90° for 3 seconds when an allowed card is shown. Pin 18 is busy (SPI clock), so put the servo's signal wire on pin **13**, red on **5V**, brown on **GND**.

!!! challenge "Bonus: Intruder alarm"
    Count wrong cards in a row. After 3 wrong cards, flash the red LED and sound a siren.

## 7. Quiz

!!! question "Check what you learned"
    1. Why doesn't an RFID card need a battery?
    @lines 2
    2. Why must the RC522 be connected to 3V3 and not 5V?
    @lines 1
    3. What does `return` do inside `loop()`?
    @lines 1
    4. Is a UID a good password? Why or why not? *(Hint: could someone copy it?)*
    @lines 2

**Tidy up:** unplug the USB cable. Put the card and tag back in the kit. You can leave the reader wired up.
