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
	pytest -x -v

.PHONY = $(VENV)/bin/activate
$(VENV)/bin/activate: requirements.txt
	$(PYTHON_COMMAND) -m venv $(VENV)
	$(PIP_COMMAND) install -r requirements.txt

.PHONY = build-reqs
build-reqs:
	$(PIP_COMMAND) install pipreqs
	pipreqs . --force --encoding=utf8
	echo gunicorn==20.1.0 >> requirements.txt
	echo eventlet==0.30.2 >> requirements.txt
	echo yapf==0.32.0 >> requirements.txt
	echo psycopg2-binary==2.9.3 >> requirements.txt
	echo toml==0.10.2 >> requirements.txt
	sed -i 's/rl==3.0/keras-rl2==1.0.5/g' ./requirements.txt
	sed -i 's/python_bcrypt==0.3.2/bcrypt==3.2.0/g' ./requirements.txt
	sed -i '/server==0.0.0/d' ./requirements.txt

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

