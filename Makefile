# Build the curriculum: compile every sketch and print every handout.
# Only what changed is rebuilt. Add -j for parallel builds, e.g. `make -j6`.
#
#   make                  compile all sketches + build all handouts
#   make check            compile all sketches
#   make pdfs             build the handouts in handouts/
#   make check LESSON=L05 / make pdfs LESSON=L05   just one lesson
#   make upload SKETCH=lessons/L01-hello-esp32/L01_Blink PORT=/dev/cu.usbserial-0001

ARDUINO := tools/arduino
PYTHON  := .venv/bin/python
FQBN    := esp32:esp32:esp32
PAPER   ?= letter
PORT    ?= /dev/cu.usbserial-0001
LESSON  ?=

BUILD   := .arduino/build
STAMPS  := .arduino/stamps

LESSON_DIRS := $(patsubst %/lesson.md,%,$(wildcard lessons/*$(LESSON)*/lesson.md))
SKETCHES    := $(shell find $(LESSON_DIRS) -name '*.ino' | sort)
COMPILED    := $(patsubst %.ino,$(STAMPS)/%.ok,$(SKETCHES))
HANDOUTS    := $(patsubst lessons/%,handouts/%.pdf,$(LESSON_DIRS))
BOOK        := handouts/ESP32-Curriculum-All-Lessons.pdf
PDF_TOOLS   := tools/build_pdfs.py tools/handout.css

.PHONY: all check pdfs book setup intellisense ports upload monitor clean
.DELETE_ON_ERROR:

all: check pdfs

check: $(COMPILED)
	@echo "$(words $(COMPILED)) sketches compile."

pdfs: $(HANDOUTS) $(if $(LESSON),,$(BOOK))

book: $(BOOK)

# One stamp per sketch; rebuilt when any file in the sketch folder changes.
.SECONDEXPANSION:
$(STAMPS)/%.ok: %.ino $$(wildcard $$(dir %)*)
	@mkdir -p $(@D)
	@$(ARDUINO) compile --fqbn $(FQBN) --build-path $(BUILD)/$(notdir $*) --warnings default $(<D) \
		> $(@:.ok=.log) 2>&1 || { grep -E 'error|Error' $(@:.ok=.log) | head -20; echo "FAIL  $(notdir $*)"; exit 1; }
	@echo "ok    $(notdir $*)"
	@touch $@

# One handout per lesson; it embeds the lesson's sketches, so it depends on them.
handouts/%.pdf: lessons/%/lesson.md $$(shell find lessons/$$* -name '*.ino') $(PDF_TOOLS)
	@mkdir -p $(@D)
	@$(PYTHON) tools/build_pdfs.py --paper $(PAPER) $*

$(BOOK): $(wildcard lessons/*/lesson.md) $(shell find lessons -name '*.ino') $(PDF_TOOLS)
	@$(PYTHON) tools/build_pdfs.py --paper $(PAPER) --book

setup:          ## ESP32 core, libraries, Python venv and VS Code IntelliSense, all inside this folder
	tools/setup.sh

intellisense:
	$(PYTHON) tools/vscode_intellisense.py

ports:
	$(ARDUINO) board list

upload:
	$(ARDUINO) compile --upload --port $(PORT) --fqbn $(FQBN) $(SKETCH)

monitor:
	$(ARDUINO) monitor --port $(PORT) --config baudrate=115200

clean:
	rm -rf $(BUILD) $(STAMPS)
