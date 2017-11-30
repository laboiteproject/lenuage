from __future__ import unicode_literals

import pytest

from .models import AppLikes


@pytest.fixture
def app(boite):
    return AppLikes.objects.create(boite=boite,
                                   page_name='page',
                                   likes=0)


@pytest.mark.django_db
def test_graph_call(app, mocker):
    mock = mocker.patch('laboite.apps.likes.models.facebook.GraphAPI.get_object',
                        return_value={'fan_count': 10})
    app.update_data()
    kwargs = sorted(mock.call_args[1].items())
    assert kwargs == [('fields', 'fan_count'), ('id', 'page')]
    assert app.likes == 10

    mock.reset_mock()
    mock.return_value = {'fan_count': 2}

    app.page_name = 'my_page'
    app.save()
    app.update_data()
    kwargs = sorted(mock.call_args[1].items())
    assert kwargs == [('fields', 'fan_count'), ('id', 'my_page')]
    assert app.likes == 2
