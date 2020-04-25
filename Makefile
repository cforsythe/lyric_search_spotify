.PHONY: run all clean

run: all app-env
	FLASK_APP=spotical_backend FLASK_ENV=development flask run
	
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	. ./venv/bin/activate; pip install -Ur requirements.txt
	touch venv/bin/activate

all: venv/bin/activate 

app-env:
	. ./app_env

clean:
	rm -rf venv
	find . -iname "*.pyc" -delete -o -iname "*.pyo" -delete
