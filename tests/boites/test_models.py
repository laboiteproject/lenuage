from datetime import timedelta

from django.utils import timezone
from boites.models import App, Boite


def test_boite_api_key(admin_user):
    """Make sure the api_key is properly set."""
    boite = Boite(name='test boite', user=admin_user)
    # Before saving the boite, no api_key is generated.
    assert boite.api_key == ''
    # One the boite is saved, an api_key is generated.
    boite.save()
    api_key = boite.api_key
    assert api_key
    # Any subsequent saves won't overwrite the generated api_key.
    boite.save()
    assert boite.api_key == api_key


def test_should_update():
    app = App()

    # Test with UPDATE_INTERVAL = None
    app.UPDATE_INTERVAL = None
    app.last_activity = None
    assert app.should_update()

    app.last_activity = timezone.now()
    assert app.should_update()

    # Test with a short UPDATE_INTERVAL but no last_activity
    app.UPDATE_INTERVAL = 1
    app.last_activity = None
    assert app.should_update()

    # Test as if it was updated recently
    app.last_activity = timezone.now()
    assert not app.should_update()
    # Wait for it to expire
    app.last_activity -= timedelta(seconds=2)
    assert app.should_update()


def test_get_data():
    ret = {'key': 'value'}

    class FailingApp(App):
        class Meta:
            app_label = 'failing app'

        def _get_data(self):
            return ret

        def update_data(self):
            raise ValueError('shit happens')

        def save(self):
            pass

    class ValidApp(App):
        class Meta:
            app_label = 'valid app'

        def _get_data(self):
            return ret

        def update_data(self):
            return True

        def save(self):
            pass

    app = FailingApp()
    app.enabled = True
    app.last_activity = None
    assert app.get_data() is None
    app.last_activity = timezone.now()
    assert app.get_data() == ret
    assert app.get_app_dictionary() is None

    app = ValidApp()
    app.enabled = True
    app.last_activity = timezone.now()
    assert app.get_data() == ret
    assert app.get_app_dictionary() == ret

    app.enabled = False
    assert app.get_data() is None
    assert app.get_app_dictionary() is None
