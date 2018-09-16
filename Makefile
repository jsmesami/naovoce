reqs:
	pip-compile --upgrade --output-file ./requirements/base.txt ./requirements/base.in
	pip-compile --upgrade --output-file ./requirements/test.txt ./requirements/test.in
	pip-compile --upgrade --output-file ./requirements/dev.txt ./requirements/dev.in

lint:
	pylint src tests

coala:
	coala --no-orig --apply-patches

test:
	PYTHONPATH=src pytest -v tests
