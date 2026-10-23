.PHONY: setup check pdfs pdfs-a4 intellisense upload monitor ports

PORT ?= /dev/cu.usbserial-0001

setup:          ## install ESP32 core, libraries and Python tools into this folder
	tools/setup.sh

check:          ## compile every sketch in lessons/
	tools/compile_all.sh

pdfs:           ## build all handouts into handouts/ (US Letter)
	.venv/bin/python tools/build_pdfs.py

pdfs-a4:        ## build all handouts on A4 paper
	.venv/bin/python tools/build_pdfs.py --paper a4

intellisense:   ## regenerate .vscode/c_cpp_properties.json
	.venv/bin/python tools/vscode_intellisense.py

ports:          ## list connected boards
	tools/arduino board list

upload:         ## make upload SKETCH=lessons/L01-hello-esp32/L01_Blink PORT=/dev/cu.usbserial-0001
	tools/arduino compile --upload --port $(PORT) --fqbn esp32:esp32:esp32 $(SKETCH)

monitor:        ## make monitor PORT=...
	tools/arduino monitor --port $(PORT) --config baudrate=115200
