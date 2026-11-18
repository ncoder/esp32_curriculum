"""Lesson 17 circuits: RC522 RFID reader on SPI, then the red/green LEDs and buzzer."""
from circuits import Circuit
from circuits.kit import buzzer_side, gnd_a, gnd_b, led_a

c = Circuit("L17_reader", "RC522: SDA 5, SCK 18, MOSI 23, MISO 19, RST 4, power 3V3 only",
            sketches=["L17_ReadCard"])
gnd_b(c)
# The reader hangs below board B on female-to-male wires (pins right to left: SDA ... 3.3V).
c.module("U1", "rc522", (20, 41.5), rotate=180)
c.wire("U1.SDA", "B:e8", bulge=0.6)       # SS  <- 5
c.wire("U1.SCK", "B:d9", bulge=0.6)       # SCK <- 18
c.wire("U1.MOSI", "B:c15", bulge=-0.4)    # MOSI <- 23
c.wire("U1.MISO", "B:b10", bulge=0.6)     # MISO <- 19
c.wire("U1.GND", "B:-15")
c.wire("U1.RST", "B:e5", bulge=0.6)       # RST <- 4
c.wire("U1.3.3V", "B:e1", bulge=0.6)      # 3V3 only!
c.schematic.module("U1", left=[("SDA", 5), ("SCK", 18), ("MOSI", 23), ("MISO", 19), ("RST", 4)],
                   top=[("3.3V", "3V3")], bottom=[("GND", "GND")], title="RC522 RFID",
                   note="IRQ is not connected")

a = c.copy("L17_access", "Access control: + red LED on 25, green LED on 27, buzzer on 33",
           sketches=["L17_Access"])
gnd_a(a)
led_a(a, "R1", "D1", "red", 25, 10)
led_a(a, "R2", "D2", "green", 27, 6)
buzzer_side(a)
