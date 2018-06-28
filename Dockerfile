FROM debian:jessie
MAINTAINER LaBoîte Team <support@laboite.cc>
RUN apt-get update
RUN apt-get install -y build-essential libssl-dev git python python-setuptools libxslt1-dev python2.7-dev zlib1g-dev libjpeg-dev libcurl4-openssl-dev
EXPOSE 8888
ADD . /laboite
RUN cd /laboite \
    && pip install -r requirements/requirements.txt
CMD cd /laboite \
    && python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py loaddata sites \
    && python manage.py createsuperuser --username admin --email root@localhost --noinput \
    && python manage.py runserver 0.0.0.0:8888

