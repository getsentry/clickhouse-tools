install:
	pip install -r requirements.txt
	pip install `grep ^-- requirements.txt` -e .
.PHONY: install