#!/usr/bin/env bash
# Compiles every sketch in lessons/ for the ESP32 Dev Module.
# Usage: tools/compile_all.sh [filter]   e.g. tools/compile_all.sh L05
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FQBN="${FQBN:-esp32:esp32:esp32}"
FILTER="${1:-}"
BUILD="$ROOT/.arduino/build"
pass=0; fail=0; failed=()

while IFS= read -r ino; do
  dir="$(dirname "$ino")"
  name="$(basename "$dir")"
  if [ "$(basename "$ino" .ino)" != "$name" ]; then
    echo "FAIL  $name  (sketch file must be named $name.ino)"; fail=$((fail+1)); failed+=("$name"); continue
  fi
  case "$ino" in *"$FILTER"*) ;; *) continue ;; esac
  if out="$("$ROOT/tools/arduino" compile --fqbn "$FQBN" --build-path "$BUILD/$name" --warnings default "$dir" 2>&1)"; then
    echo "ok    $name"; pass=$((pass+1))
  else
    echo "FAIL  $name"; echo "$out" | grep -E "error|Error" | head -20; fail=$((fail+1)); failed+=("$name")
  fi
done < <(find "$ROOT/lessons" -name '*.ino' | sort)

echo
echo "$pass compiled, $fail failed"
[ "$fail" -eq 0 ] || { printf '  %s\n' "${failed[@]}"; exit 1; }
