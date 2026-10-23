#!/usr/bin/env bash
# One-time setup: ESP32 board core + every library the lessons use, plus the
# Python environment for building the PDF handouts.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
A="$ROOT/tools/arduino"

"$A" core update-index
"$A" core install esp32:esp32
while read -r lib; do
  [ -z "$lib" ] || [ "${lib#\#}" != "$lib" ] && continue
  "$A" lib install "$lib"
done < "$ROOT/libraries.txt"

python3 -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/pip" install -q -r "$ROOT/tools/requirements.txt"
"$ROOT/.venv/bin/python" "$ROOT/tools/vscode_intellisense.py"
echo "Setup complete."
