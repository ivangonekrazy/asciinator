.PHONY: test start lint
test:
	python -munittest tests

lint:
	pylint asciinator

start:
	FLASK_APP=asciinator/service.py FLASK_DEBUG=1 flask run
