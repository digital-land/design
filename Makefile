.PHONY: init check snapshot

init::
	pip install -r requirements.txt

check::
	python3 bin/check.py

snapshot::
	python3 bin/govuk-planning.py
