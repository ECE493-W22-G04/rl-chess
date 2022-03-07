SHELL := /bin/bash
VENV = venv
include .env

.PHONY = start
start: $(VENV)/bin/activate
	$(PYTHON_COMMAND) main.py

.PHONY = prod
prod: $(VENV)/bin/activate
	gunicorn --worker-class eventlet -w 1 main:app -b 0.0.0.0:5555

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

.PHONY = format
format:
	$(PIP_COMMAND) install yapf
	yapf -r -i .

.PHONY = clean
clean:
	rm -rf __pycache__
	rm -rf venv
	rm -rf _logs
	rm -rf .pytest_cache
