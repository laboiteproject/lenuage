import pytest

from boites.models import Boite
from app_parcel.models import AppParcel


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


def test_get_app_dictionnary(parcel):
    assert parcel.get_app_dictionary() == {
        "arrival": None,
        "info": None,
        "parcel": "parcel to track",
        "status": None,
        "parcel_carrier": "chronopost",
    }


def test_get_apps_dictionnary_single_app(parcel):
    assert parcel.boite.get_apps_dictionary() == {
        "app_parcel": [
            {
                "arrival": None,
                "info": None,
                "parcel": "parcel to track",
                "status": None,
                "parcel_carrier": "chronopost",
            }
        ]
    }


def test_get_apps_dictionnary_duplicated_apps(parcel):
    parcel2 = parcel
    parcel2.id = None
    parcel2.save()  # Hack: save parcel2 as a new instance.
    parcel2.parcel = "another parcel to track"
    parcel2.parcel_carrier = "gls"
    parcel2.save()
    assert parcel.boite.get_apps_dictionary() == {
        "app_parcel": [
            {
                "arrival": None,
                "info": None,
                "parcel": "parcel to track",
                "status": None,
                "parcel_carrier": "chronopost",
            },
            {
                "arrival": None,
                "info": None,
                "parcel": "another parcel to track",
                "status": None,
                "parcel_carrier": "gls",
            },
        ]
    }
