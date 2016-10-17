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


## Creating your own app

You can use [cookiecutter](https://cookiecutter.readthedocs.io/) to help you
create a minimalist scaffolding for your own app.

Let's create a "message of the day" app that will allow you to specify a
message to display. Start by creating the files using cookiecutter:

```
cookiecutter cookiecutter_app/
```

You will get prompted to enter a few names:
- `app_name [lowercase_no_spaces]: motd`
- `app_model_name [CamelCaseNoSpaces]: MotD`
- `app_verbose_name [Some verbose name]: Message of the Day`


### Edit your model

You can now edit the newly created `app_motd/models.py` file (we don't need to
do any "updating", so we can skip the "only update any X minutes" part):

```python
class AppMotD(App):
    motd = models.CharField(_(u'Message'), blank=True, null=True)

    def get_app_dictionary(self):
        if not self.enabled:
            return

        return {'data': self.motd}

    class Meta:
        verbose_name = _("Configuration : Message of the Day")
        verbose_name_plural = _("Configurations : Message of the Day")
```


### Add your new app to the settings

Edit the `laboite/settings.py` file, and add your app name to the list of existing `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...

    # laboite apps
    "app_time",
    "app_weather",
    "app_parcel",
    "app_tasks",
    "app_traffic",
    "app_alarm",
    "app_motd",  ## <---- make sure you add your app name to the list!
]
```


### Create and run your migration

Django needs a migration to know how to update your database. However, it's
usually smart enough to create this migration for you!

```
./manage.py makemigrations app_motd
./manage.py migrate
```


### Profit!

You can now go to [the admin](http://127.0.0.1:8000/admin), and add a "motd
app" for your *boite*.

Make sure the message you added is displayed in the json displayed on the
*boite* page:
http://127.0.0.1:8000/boites/1/json (replace `1` with the id of your *boite*)

```
{

    ...
    "app_motd": [
        {
            "data": "This is my test message of the day!"
        }
    ],
    ...
}
```
