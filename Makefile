.PHONY: run all clean


run: all
	FLASK_APP=flaskr FLASK_ENV=development flask run
	
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -Ur requirements.txt
	touch venv/bin/activate

all: venv/bin/activate 

clean:
	rm -rf venv
	find . -iname "*.pyc" -delete -o -iname "*.pyo" -delete
