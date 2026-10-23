# Lesson 10 teacher notes

**Before class:** install **Adafruit SSD1306** (with its dependencies,
*Adafruit GFX Library* and *Adafruit BusIO*) on every computer if the
classroom network is slow. Check one screen with L10_Hello. The kit screen
is assumed to be an SSD1306 at I²C address 0x3C; a few modules are 0x3D.

**If the picture is garbled or shifted by 2 pixels,** the module is probably
an SH1106, not an SSD1306. It needs a different library (e.g. *Adafruit
SH110X*), so let us know and we'll add a variant.

**Common problems**

- *Screen stays dark:* SDA/SCL swapped, VCC on the wrong rail, or a
  different address. The module's pin order varies (GND-VCC-SCL-SDA is
  common, but some start with VCC), so students must read the labels.
- *Compile error `Adafruit_SSD1306.h: No such file`:* the library isn't
  installed, or the student clicked "Install without dependencies". Install
  *Adafruit GFX Library* too.
- *Screen dark although the wiring is right:* the student forgot
  `display.display()`.
- *The counter overwrites itself into a white blob:* `clearDisplay()` is
  missing.
- *Bounce: the ball leaves the screen and gets stuck at an edge:* `dx = -dx`
  is inside the wrong `if`, or students used `<` with a start position
  outside the box.

**Quiz answers**

1. It gives you ready-made code, here the commands to draw text and shapes,
   so you don't have to write it yourself.
2. (127, 63).
3. Drawing only changes the picture in the ESP32's memory;
   `display.display()` sends it to the screen.

**Challenge solutions:** `solutions/L10_BarGraph` (challenge 2) and
`solutions/L10_Paddle` (bonus). Challenge 3 duplicates the four variables,
the two `if`s and the `fillCircle`.

**Leave it wired:** Lesson 11 uses the same screen on the same pins.
