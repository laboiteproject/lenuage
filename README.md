[![Build Status](https://travis-ci.org/bgaultier/laboitepro.svg?branch=master)](https://travis-ci.org/bgaultier/laboitepro)

# laboîte
Django web app of the laboîte project http://laboite.cc/help

## Getting Started

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`) and the following packages are installed :
* pytz
* jsonfield
* django-openid-auth
* libxslt1-dev
* python3-dev
* zlib1g-dev
* libjpeg-dev

For exemple on linux distributions, use:
```
apt-get install pytz jsonfield django-openid-auth libxslt1-dev python3-dev zlib1g-dev libjpeg-dev
```

```
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata sites
./manage.py createsuperuser
./manage.py runserver
```

You can then connect to the admin on http://127.0.0.1:8000/admin with the super
user you created above.
