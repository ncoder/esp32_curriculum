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
button(p, "SW1", 13, "A:e21", to=("A:i5", "A:i21"), bend=0)
button(p, "SW2", 14, "A:e25", to=("A:h8", "A:h25"), bend=0)
button(p, "SW3", 16, "B:e20", to=("B:b8", "B:b20"), bend=0)
button(p, "SW4", 17, "B:e24", to=("B:c9", "B:c24"), bend=0)
button(p, "SW5", 18, "B:e28", to=("B:d11", "B:d28"), bend=0)
