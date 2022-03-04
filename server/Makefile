SHELL := /bin/bash
VENV = venv
include .env
PYTHON_COMMAND := python3
PIP_COMMAND := pip3

.PHONY = start
start: $(VENV)/bin/activate
	$(PYTHON_COMMAND) main.py

.PHONY = test
test: $(VENV)/bin/activate
	pytest -v

.PHONY = $(VENV)/bin/activate
$(VENV)/bin/activate: requirements.txt
	$(PYTHON_COMMAND) -m venv $(VENV)
	$(PIP_COMMAND) install -r requirements.txt

.PHONY = build-reqs
build-reqs:
	$(PIP_COMMAND) install pipreqs
	pipreqs . --force

.PHONY = clean
clean:
	rm -rf __pycache__
	rm -rf venv
	rm -rf _logs
	rm -rf .pytest_cache
