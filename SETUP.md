# Setting up the computers

## Student computers (Arduino IDE only)

Students only need the plain Arduino IDE. Do this once per computer before
Lesson 1.

1. Install **Arduino IDE 2** from <https://www.arduino.cc/en/software>.
2. **File → Preferences → Additional boards manager URLs**, add:
   `https://espressif.github.io/arduino-esp32/package_esp32_index.json`
3. **Tools → Board → Boards Manager**: install **esp32 by Espressif Systems**
   (version 3.x; the lessons were tested with 3.3.12). It is a large download.
4. **Tools → Manage Libraries…**: install each library in
   [libraries.txt](libraries.txt). When the IDE asks to install dependencies,
   choose **Install all**:
   - Adafruit SSD1306 (pulls in Adafruit GFX Library and Adafruit BusIO)
   - DHT sensor library (pulls in Adafruit Unified Sensor)
   - ESP32Servo
   - Keypad (by Mark Stanley and Alexander Brevig)
   - MFRC522 (by GithubCommunity / miguelbalboa)
   - IRremote (by Armin Joachimsmeyer, version 4.x)
5. Plug in a board and check that a port appears under **Tools → Port**. If it
   doesn't, install the **CP210x USB to UART driver** from Silicon Labs.
6. Select **Tools → Board → esp32 → ESP32 Dev Module**.

Each lesson tells students when a library is first needed, so you can also
install the libraries during class as a teaching moment. Installing them
beforehand saves time.

To open a finished solution in the IDE, use **File → Open…** and pick the
`.ino` file inside `lessons/…`. The IDE requires each sketch to sit in a
folder with the same name, and every solution already does.

## Teacher / maintainer computer (this repository)

Needs macOS or Linux (or Git Bash/WSL on Windows), Python 3.9+, Google Chrome
(for printing PDFs) and either `arduino-cli` or Arduino IDE 2 (the scripts use
the copy of `arduino-cli` bundled inside the IDE).

```sh
make setup     # ESP32 core + libraries into .arduino/, Python venv, VS Code IntelliSense
make check     # compile every sketch
make pdfs      # rebuild every handout in handouts/ (make pdfs-a4 for A4 paper)
```

Everything is installed inside this folder (`.arduino/`, `.venv/`), so your
own Arduino IDE setup is left alone.

### VS Code

Open the folder in VS Code and install the recommended **C/C++** extension.
With a sketch's `.ino` file open, use **Terminal → Run Task…**:

| Task | What it does |
|---|---|
| Arduino: compile this sketch (also Cmd/Ctrl+Shift+B) | Compiles the open sketch for the ESP32 Dev Module |
| Arduino: upload this sketch | Compiles and uploads; asks for the serial port |
| Arduino: serial monitor | Opens the serial monitor at 115200 baud |
| Arduino: list connected boards | Shows which port your board is on |
| Check: compile all lessons | Compiles every sketch |
| Handouts: build PDFs | Rebuilds every handout |
| IntelliSense: refresh | Regenerates the code-completion config |
