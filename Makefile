.PHONY: run all clean

SHELL := /bin/bash

run: app-env activate
	FLASK_APP=spotical_backend FLASK_ENV=development flask run
	
create_venv: 
	test -d venv || virtualenv venv
	touch venv/bin/activate

reqs_install: requirements.txt activate
	pip3 install -Ur requirements.txt

activate: create_venv 
	. venv/bin/activate

all: create_venv reqs_install 

app-env:
	. app_env

clean:
	rm -rf venv
	find . -iname "*.pyc" -delete -o -iname "*.pyo" -delete
