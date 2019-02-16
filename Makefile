.PHONY: reqs
reqs:
	pip-compile --upgrade --output-file ./requirements/base.txt ./requirements/base.in
	pip-compile --upgrade --output-file ./requirements/dev.txt ./requirements/dev.in
	pip-compile --upgrade --output-file ./requirements/lint.txt ./requirements/lint.in
	pip-compile --upgrade --output-file ./requirements/test.txt ./requirements/test.in

.PHONY: lint
lint:
	PYTHONPATH=src pylint src tests

.PHONY: coala
coala:
	coala --no-orig --apply-patches

.PHONY: test
test:
	PYTHONPATH=src pytest -vv --cov=src tests
	rm -rf tests/media/
