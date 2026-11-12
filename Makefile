.PHONY: init check snapshot legislation terms dataset review

init::
	pip install -r requirements.txt

check::
	python3 bin/check.py

snapshot::
	python3 bin/govuk-planning.py

legislation::
	./bin/legislation-fetch.sh

terms::
	python3 bin/nppf-glossary.py
	python3 bin/legislation-terms.py --all --with-nppf
	python3 bin/build-terms.py
	python3 bin/abbreviations.py

review::
	python3 bin/dataset-review.py

dataset::
	python3 bin/dataset.py
	python3 bin/term-usage.py
