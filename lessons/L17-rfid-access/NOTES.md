# Lesson 17 teacher notes

**Before class:** check each kit has its RC522 card and key tag. The RC522 in
some kits comes with its header pins loose; if so they must be soldered
before class (bent loose pins give flaky reads). Pre-install the **MFRC522**
library if your computers have no internet.

**Wiring:** SPI pins are fixed (SCK 18, MISO 19, MOSI 23); SDA/SS is on 5,
RST on 4. Power from **3V3 only**. The servo extension uses pin 13 because 18
is the SPI clock.

**Common problems**

- *Nothing ever reads:* MISO and MOSI swapped, or SDA not on 5. Check
  `rfid.PCD_DumpVersionToSerial();` in `setup()`. It should print a firmware
  version, not `0x00` or `0xFF` (which means a wiring fault).
- *Reads once, then never again:* a card held still is only read once by
  design (`PICC_HaltA`). Take it away and bring it back.
- *Allowed card denied:* typo in the UID string. Copy/paste from the Serial
  Monitor is easiest.
- *Buzzer silent:* active buzzers also work with `tone()` but sound the same
  pitch; a passive one gives the two tones.

**Discussion point (quiz 4):** a UID is not a secret. Cheap phones and
gadgets can read and copy it, which is why real systems use encrypted cards.
Good chat about security.

**Quiz answers**

1. The reader's radio wave makes electricity in the card's coil, powering the chip.
2. The RC522 is a 3.3 V part; 5 V can damage it.
3. It ends this run of `loop()` immediately; `loop()` then starts again.
4. Not really. The UID can be read by anyone with a reader and some cards can
   be cloned; it's an ID, not a secret.

**Challenge solutions:** `solutions/L17_Door` (servo door + 3-strikes alarm).
Challenges 1 and 2 are small edits to `L17_Access`: for 2, add
`String names[] = {"Sam", "Alex"};` and change `isAllowed` to return the
index (or -1).
