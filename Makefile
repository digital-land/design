.PHONY: init check govuk legislation terms dataset review doctate

all::  check review

check::
	python3 bin/check.py

init::
	pip install -r requirements.txt

govuk::
	python3 bin/govuk-planning.py

legislation::
	./bin/legislation-fetch.sh

terms::
	python3 bin/nppf-glossary.py
	python3 bin/legislation-terms.py --all --with-nppf
	python3 bin/build-terms.py
	python3 bin/term-fields.py
	python3 bin/govuk-ensure.py
	python3 bin/abbreviations.py

review::
	python3 bin/dataset-review.py

dataset::
	python3 bin/dataset.py
	python3 bin/term-usage.py

doctate::
	python3 bin/doctate.py
