"""Lesson 6 circuits: a buzzer on 33, then five piano buttons."""
from circuits import Circuit
from circuits.kit import button, buzzer33, gnd_a, gnd_b

c = Circuit("L06_beep", "Active buzzer on pin 33", sketches=["L06_Beep"])
gnd_a(c)
buzzer33(c, active=True)

p = Circuit("L06_piano", "Passive buzzer on 33 + five buttons on 13, 14, 16, 17, 18",
            sketches=["L06_Melody", "L06_Piano"])
gnd_a(p)
gnd_b(p)
buzzer33(p, active=False)
button(p, "SW1", 13, "A:e20", to=("A:i3", "A:i20"), bend=0)
button(p, "SW2", 14, "A:e24", to=("A:h5", "A:h24"), bend=0)
button(p, "SW3", 16, "B:e18", to=("B:b6", "B:b18"), bend=0)
button(p, "SW4", 17, "B:e22", to=("B:c7", "B:c22"), bend=0)
button(p, "SW5", 18, "B:e26", to=("B:d9", "B:d26"), bend=0)
