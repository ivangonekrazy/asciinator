.PHONY: test start
test:
	python -munittest tests

start:
	FLASK_APP=asciinator/service.py FLASK_DEBUG=1 flask run
