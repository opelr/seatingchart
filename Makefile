.PHONY: all

all: format test

format:
	@poetry run black --target-version py36 seatingchart.py
	@poetry run flake8 "--ignore=E203,E402,E501,F405,W503,W504" seatingchart.py
	@poetry run black --target-version py36 tests
	@poetry run flake8 "--ignore=E203,E402,E501,F405,W503,W504" tests

test:
	@poetry run pytest
