Installation
============

## Prerequisities

* Python 3.9+
* PostgreSQL 12+ with PostGIS and HStore
* GEOS

## Very basic local installation example

	# Create and activate virtualenv with the latest Python 3 you have:
	mkdir ~/.env
	python3 -m venv ~/.env/naovoce
	source ~/.env/naovoce/bin/activate

	# Upgrade pip:
	pip install --upgrade pip

	# Install site and dependencies:
	git clone https://github.com/jsmesami/naovoce.git
	cd naovoce
	pip install -r requirements.txt

	# Create and edit local settings to match your setup: 
	cp src/naovoce/settings/[prod|dev]_example.py src/naovoce/settings/local.py
	vim src/naovoce/settings/local.py

	# Create database to match your settings, eg.:
	psql -c "CREATE USER naovoce WITH PASSWORD 'secret'"
	psql -c "CREATE DATABASE naovoce OWNER=naovoce"
	psql -c "CREATE EXTENSION postgis" naovoce
	psql -c "CREATE EXTENSION hstore" naovoce
	
	# Populate database:
	chmod u+x src/manage.py
	src/manage.py migrate
	src/manage.py loaddata fixtures/sites.json
	src/manage.py loaddata fixtures/kinds.json
	src/manage.py createsuperuser
	
	# In case you point your STATIC_ROOT outside of the project, you will need to run collectstatic:
	src/manage.py collectstatic
