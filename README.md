Na-ovoce.cz
===========

Na ovoce aims to become a web community platform that maps fruit trees, fruit bushes and 
herbs in wild and public spaces. At the same time its activities increase awareness 
of traditional varieties among the general public and contribute to their retention 
in the landscape. For more info please visit [About Us](https://na-ovoce.cz/en/about-us/).

## Installation

Prerequisities:

* Python3.4+
* PostgreSQL
* CoffeeScript
* Less
* Bower


Installation on shared hosting without Node (and no root privileges):

	# Create and activate virtualenv with the latest Python 3 you have.
	mkdir ~/.env
	python3[.5] -m venv ~/.env/naovoce
	source ~/.env/naovoce/bin/activate

	# Upgrade pip.
	pip install --upgrade pip
	
	# Install Node prerequisities into your virtualenv.
	pip install nodeenv
	nodeenv -p --prebuilt
	npm install -g coffee-script less bower

	# Install site and dependencies.
	git clone https://github.com/jsmesami/naovoce.git
	cd naovoce
	pip install -r requirements.txt [-b ~/tmp]
	bower install

	# Create and edit local settings to match your setup. 
	cd src
	cp naovoce/settings/local_[deploy|devel]_example.py naovoce/settings/local.py
	vim naovoce/settings/local.py

	# Prepare database and load initial data.
	chmod u+x manage.py
	./manage.py migrate
	./manage.py loaddata naovoce/fixtures/sites.json
	./manage.py loaddata fruit/fixtures/kinds.json
	./manage.py loaddata staticpage/fixtures/staticpages.json
	./manage.py createsuperuser
	./manage.py collectstatic
