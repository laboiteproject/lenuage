from uuid import uuid4

import pytest
from requests_mock import Mocker

from boites.models import Boite


@pytest.fixture
def boite(admin_user):
    """Returns a test boite object"""
    return Boite.objects.create(name='test boite', user=admin_user, api_key=uuid4())


@pytest.fixture
def requests_mocker():
    return Mocker()
