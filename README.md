# KIFPLAN

Django-Webapplikation zur Planung einer KIF

## Development

* (optional) Create a new virtualenv `virtualenv env -p python3`
* (optional) Activate vairtualenv `source env/bin/activate`
* Install python dependencies `pip install -r requirements.txt`
* apply migrations `./manage.py migrate`
* Run a local server with `./manage.py runserver`
* Access your local instance by opening `http://127.0.0.1:8000/` in your webbrowser

## Deployment

### Installation

* Install `python3`, `python3-pip`, `python3-virtualenv`
* Clone this repository into a proper directory (e.g. `/srv/kiffel-verwaltung`)
* Create the file `kiffelverwaltung/settings_local.py` and fill it with production settings (it will be included automatically and overrides default settings)
* Create a virtualenv (e.g. `virtualenv -p python3 venv`)
* For serving WSGI applications, one can install `uwsgi`, create an ini file under `/etc/uwsgi/` with the proper configuration and configure the webserver to use mod-proxy-uwsgi to make the application accessible. The webserver should also serve the static files.
* Run all the relevant commands from the Updates section

### Updates

* `systemctl stop uwsgi`
* `git pull`
* `source venv/bin/activate` when one of the `pip` or `./manage.py` steps are necessary
* `pip install -r requirements.txt` when the `requirements.txt` file changed
* `./manage.py migrate` when a new migrations file is available
* `./manage.py collectstatic` when a static file changed (or `bower install` was run)
* `./manage.py compilemessages` when a message file (`*.po`) changed
* `deactivate` when virtualenv was activated
* `chown -R django:django .`
* `systemctl start uwsgi`
