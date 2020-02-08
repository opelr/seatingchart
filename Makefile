.PHONY: all

all: format test

format:
	@poetry run black seatingchart.py
	@poetry run flake8 "--ignore=E203,E402,E501,F405,W503,W504" seatingchart.py
	@poetry run black tests
	@poetry run flake8 "--ignore=E203,E402,E501,F405,W503,W504" tests

test:
	@poetry run pytest
