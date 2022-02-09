SHELL := /bin/bash
VENV = venv
include .env

start: $(VENV)/bin/activate
	$(PYTHON_COMMAND) main.py

test: $(VENV)/bin/activate
	pytest -v

$(VENV)/bin/activate: requirements.txt
	$(PYTHON_COMMAND) -m venv $(VENV)
	$(PIP_COMMAND) install -r requirements.txt

build-reqs:
	$(PIP_COMMAND) install pipreqs
	pipreqs . --force

clean:
	rm -rf __pycache__
	rm -rf venv
	rm -rf _logs
	rm -rf .pytest_cache