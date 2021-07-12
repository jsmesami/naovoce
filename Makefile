.PHONY: reqs
reqs:
	pip-compile --upgrade --output-file ./requirements/base.txt ./requirements/base.in
	pip-compile --upgrade --output-file ./requirements/dev.txt ./requirements/dev.in
	pip-compile --upgrade --output-file ./requirements/lint.txt ./requirements/lint.in
	pip-compile --upgrade --output-file ./requirements/test.txt ./requirements/test.in

.PHONY: isort
isort:
	isort --skip migrations --profile django -e -m 3 -w 120 src tests

.PHONY: black
black:
	black --exclude migrations -l 120 src tests

.PHONY: lint
lint:
	flake8 src tests

.PHONY: test
test:
	PYTHONPATH=src pytest -vv --ds=naovoce.settings.test --cov=src tests
	rm -rf tests/media/
