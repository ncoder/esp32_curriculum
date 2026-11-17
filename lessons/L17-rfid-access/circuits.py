"""Lesson 17 circuits: RC522 RFID reader on SPI, then the red/green LEDs and buzzer."""
from circuits import Circuit
from circuits.kit import buzzer_side, gnd_a, gnd_b, led_a

c = Circuit("L17_reader", "RC522: SDA 5, SCK 18, MOSI 23, MISO 19, RST 4, power 3V3 only",
            sketches=["L17_ReadCard"])
gnd_b(c)
# The reader hangs below board B on female-to-male wires (pins right to left: SDA ... 3.3V).
c.module("U1", "rc522", (20, 41.5), rotate=180)
c.wire("U1.SDA", "B:e10", bulge=0.8)      # SS  <- 5
c.wire("U1.SCK", "B:d11", bulge=0.8)      # SCK <- 18
c.wire("U1.MOSI", "B:c18", bulge=-0.6)    # MOSI <- 23
c.wire("U1.MISO", "B:b12", bulge=0.8)     # MISO <- 19
c.wire("U1.GND", "B:-15")
c.wire("U1.RST", "B:e7", bulge=0.8)       # RST <- 4
c.wire("U1.3.3V", "A:i19", via=[(13.0, 36.6), (20.6, 36.6), (20.6, 14.0)])   # 3V3 only!
c.schematic.module("U1", left=[("SDA", 5), ("SCK", 18), ("MOSI", 23), ("MISO", 19), ("RST", 4)],
                   top=[("3.3V", "3V3")], bottom=[("GND", "GND")], title="RC522 RFID",
                   note="IRQ is not connected")

a = c.copy("L17_access", "Access control: + red LED on 25, green LED on 27, buzzer on 33",
           sketches=["L17_Access"])
gnd_a(a)
led_a(a, "R1", "D1", "red", 11, 12, schematic_gpio=25)
led_a(a, "R2", "D2", "green", 9, 8, schematic_gpio=27)
buzzer_side(a)
