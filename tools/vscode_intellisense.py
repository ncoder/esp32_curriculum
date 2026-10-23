#!/usr/bin/env python3
"""Generates .vscode/c_cpp_properties.json so VS Code's C/C++ extension understands
the sketches (Arduino.h, the ESP32 core and every library in libraries.txt).

It compiles a throwaway sketch that includes every library header with
--only-compilation-database, then turns the compiler flags into include paths and
defines. Re-run it after changing the core or libraries (VS Code task:
"IntelliSense: refresh").
"""
import json
import shlex
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEADERS = ["Wire.h", "SPI.h", "WiFi.h", "WebServer.h", "Adafruit_GFX.h", "Adafruit_SSD1306.h",
           "DHT.h", "ESP32Servo.h", "Keypad.h", "MFRC522.h", "IRremote.hpp"]


def expand(args):
    """Inline @response-file arguments (the esp32 core keeps most flags in files)."""
    out = []
    for a in args:
        if a.startswith("@") and Path(a[1:]).is_file():
            out += expand(shlex.split(Path(a[1:]).read_text()))
        else:
            out.append(a)
    return out


def main():
    with tempfile.TemporaryDirectory() as tmp:
        sketch = Path(tmp) / "probe"
        sketch.mkdir()
        (sketch / "probe.ino").write_text("".join(f"#include <{h}>\n" for h in HEADERS) + "void setup(){}\nvoid loop(){}\n")
        build = Path(tmp) / "build"
        subprocess.run([str(ROOT / "tools" / "arduino"), "compile", "--fqbn", "esp32:esp32:esp32",
                        "--only-compilation-database", "--build-path", str(build), str(sketch)],
                       check=True, capture_output=True)
        db = json.loads((build / "compile_commands.json").read_text())
        entry = next(e for e in db if e["file"].endswith("probe.ino.cpp"))
        args = expand(entry["arguments"])

    includes, defines, prefix = [], [], ""
    i = 0
    while i < len(args):
        a = args[i]
        if a == "-iprefix":
            prefix = args[i + 1]; i += 1
        elif a == "-iwithprefixbefore":
            includes.append(prefix + args[i + 1]); i += 1
        elif a.startswith("-iwithprefixbefore"):
            includes.append(prefix + a[len("-iwithprefixbefore"):])
        elif a.startswith("-I") and len(a) > 2:
            includes.append(a[2:])
        elif a == "-I":
            includes.append(args[i + 1]); i += 1
        elif a.startswith("-D"):
            defines.append(a[2:])
        i += 1
    # Paths inside the throwaway build dir are gone now; keep the real ones.
    includes = [p for p in dict.fromkeys(includes) if Path(p).exists()]

    config = {
        "version": 4,
        "configurations": [{
            "name": "ESP32 (Arduino)",
            "compilerPath": args[0],
            "cStandard": "gnu17",
            "cppStandard": "gnu++20",
            "intelliSenseMode": "gcc-x86",
            "includePath": includes,
            "forcedInclude": [next(str(p) for p in map(Path, includes) if (p / "Arduino.h").exists()) + "/Arduino.h"],
            "defines": defines,
        }],
    }
    out = ROOT / ".vscode" / "c_cpp_properties.json"
    out.write_text(json.dumps(config, indent=2) + "\n")
    print(f"wrote {out.relative_to(ROOT)} ({len(includes)} include paths, {len(defines)} defines)")


if __name__ == "__main__":
    main()
