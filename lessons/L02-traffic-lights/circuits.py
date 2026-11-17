"""Lesson 2 circuit: traffic light LEDs on pins 25, 26, 27."""
from circuits import Circuit
from circuits.kit import gnd_a, traffic_leds

c = Circuit("L02_traffic", "Traffic light: red 25, yellow 26, green 27",
            sketches=["L02_TrafficLight", "L02_LightFunction", "L02_Chase"])
traffic_leds(c)
gnd_a(c)
