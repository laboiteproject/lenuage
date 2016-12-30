import pytest

from boites.models import App, Boite
from laboite.apps.parcel.models import AppParcel


@pytest.fixture
def boite(admin_user):
    boite, _ = Boite.objects.get_or_create(
        name="Test boite",
        user=admin_user,
        api_key = "123")
    yield boite


@pytest.fixture
def parcel(boite):
    parcel = AppParcel.objects.create(
        boite=boite,
        parcel="parcel to track",
        parcel_carrier="chronopost")
    yield parcel


def test_get_app_dictionary(parcel):
    assert parcel.get_app_dictionary() == {
        "arrival": None,
        "info": None,
        "parcel": "parcel to track",
        "status": None,
        "parcel_carrier": "chronopost",
    }


def test_get_apps_dictionary_single_app(parcel):
    assert parcel.boite.get_apps_dictionary() == {
        "laboite.apps.parcel": [
            {
                "arrival": None,
                "info": None,
                "parcel": "parcel to track",
                "status": None,
                "parcel_carrier": "chronopost",
            }
        ]
    }


def test_boite_api_key(admin_user):
    """Make sure the api_key is properly set."""
    boite = Boite(name="test boite", user=admin_user)
    # Before saving the boite, no api_key is generated.
    assert boite.api_key == ''
    # One the boite is saved, an api_key is generated.
    boite.save()
    api_key = boite.api_key
    assert api_key
    # Any subsequent saves won't overwrite the generated api_key.
    boite.save()
    assert boite.api_key == api_key


def test_get_app_dictionary_base_app(boite):
    app = App(boite=boite)
    with pytest.raises(NotImplementedError):
        # The App base class should not be used.
        app.get_app_dictionary()
