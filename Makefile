reqs:
	pip-compile --upgrade --output-file ./requirements/base.txt ./requirements/base.in
	pip-compile --upgrade --output-file ./requirements/test.txt ./requirements/test.in
	pip-compile --upgrade --output-file ./requirements/dev.txt ./requirements/dev.in
