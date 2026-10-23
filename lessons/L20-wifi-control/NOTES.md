# Lesson 20 teacher notes

**Why access-point mode:** the ESP32 creates its own network
(`WiFi.softAP`), so the lesson works without the school Wi-Fi password and
without exposing devices to the school network. The ESP32 is always at
**192.168.4.1** in this mode.

**Before class:** you need one phone/tablet/laptop per group. Students'
own phones are fine. If devices are scarce, one teacher tablet can visit
each group's network in turn. Check with your school's device policy.

**Running 15+ access points in one room** works, but expect the odd slow
connection. Each student **must** pick a unique name (the sketch default
`Sparky-ESP32` will collide). Passwords must be ≥ 8 characters, or
`softAP` silently fails and no network appears.

**Common problems**

- *Network doesn't appear:* password shorter than 8 characters, or the
  sketch didn't upload. Check the Serial Monitor shows the IP.
- *Phone joins then leaves:* "no internet" auto-switching. Turn off mobile
  data, or tap "stay connected" when asked.
- *Page loads but the knob always reads 0:* pot not on 34. Only ADC1 pins
  (32–39) work while Wi-Fi is on; ADC2 pins read nothing. That's why we use 34.
- *Typed `https://`:* the ESP32 only speaks plain `http://`. Type just
  `192.168.4.1`.
- *Board resets / brown-out messages:* Wi-Fi draws current spikes; try a
  different USB port or cable.

**Quiz answers**

1. 192.168.4.1.
2. When a browser asks for the address `/off`, run the `handleOff` function.
3. `<h1>` starts the heading; `</h1>` (with the slash) ends it.
4. So each student can find and join their own ESP32, and not control
   someone else's.

**Challenge solutions:** `solutions/L20_Dashboard` covers challenges 1–3 and
the bonus (styled buttons, BEEP, auto-refresh, brightness levels via
`/dim?level=`). It uses a redirect (`303` + `Location: /`) so refreshing the
page doesn't repeat the last action, which is worth explaining to keen
students.
