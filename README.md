Na-ovoce.cz
===========

Na ovoce aims to become a web community platform that maps fruit trees, fruit bushes and 
herbs in wild and public spaces. At the same time its activities increase awareness 
of traditional varieties among the general public and contribute to their retention 
in the landscape. For more info please visit [About Us](https://na-ovoce.cz/en/about-us/).

## Installation

Prerequisities:

* Python3.4
* PostgreSQL
* CoffeeScript
* Less
* Bower


Local Installation:

	mkdir .env
	python3.4 -m venv .env/naovoce
	source .env/naovoce/bin/activate
	git clone https://github.com/jsmesami/naovoce.git
	cd naovoce
	pip3.4 install -r requirements.txt
	bower install
	cd src
	cp naovoce/settings/local_[deploy|devel]_example.py naovoce/settings/local.py
	vim naovoce/settings/local.py
	chmod u+x manage.py
	./manage.py migrate
	./manage.py loaddata naovoce/fixtures/sites.json
	./manage.py loaddata fruit/fixtures/kinds.json
	./manage.py loaddata staticpage/fixtures/staticpages.json
	./manage.py createsuperuser
	./manage.py collectstatic
