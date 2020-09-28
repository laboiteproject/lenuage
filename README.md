[![Build Status](https://api.travis-ci.org/laboiteproject/lenuage.svg?branch=master)](https://travis-ci.org/laboiteproject/lenuage)

# laboîte
Django web app of the laboîte project http://laboite.cc/help

## Getting Started

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`) and the following packages are installed :

* python3
* python3-dev
* python3-pip
* libxslt1-dev
* libxml2-dev
* zlib1g-dev
* libjpeg-dev
* libgif-dev
* libpng-dev
* libgnutls28-dev

For exemple on Debian based distributions, use:
```
apt install python3 python3-dev python3-pip libxslt1-dev libxml2-dev zlib1g-dev libjpeg-dev libgif-dev libpng-dev libgnutls28-dev 
```

```
pip3 install -r requirements.txt
python3 ./manage.py migrate
python3 ./manage.py loaddata sites
python3 ./manage.py createsuperuser
python3 ./manage.py runserver
```

You can then connect to the admin on http://127.0.0.1:8000/admin with the super
user you created above.
