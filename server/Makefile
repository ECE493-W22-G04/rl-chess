SHELL := /bin/bash
VENV = venv
include .env

.PHONY = start
start: $(VENV)/bin/activate
	pushd .. && $(PYTHON_COMMAND) -m server.main && popd

.PHONY = prod
prod: $(VENV)/bin/activate
	pushd .. && gunicorn --worker-class eventlet -w 1 server.main:app -b 0.0.0.0:5555 && popd

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
	pipreqs . --force
	echo 'gunicorn==20.1.0' >> requirements.txt
	echo 'eventlet==0.30.2' >> requirements.txt
	echo 'yapf==0.32.0' >> requirements.txt
	echo 'psycopg2==2.9.3' >> requirements.txt
	sed -i 's/python_bcrypt==0.3.2/bcrypt==3.2.0/g' requirements.txt

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
