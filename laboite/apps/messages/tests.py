from __future__ import unicode_literals

from .models import AppMessages


def test_message(boite):
    app = AppMessages.objects.create(boite=boite, message='hello world')
    result = app.get_app_dictionary()
    assert len(result) == 3
    assert result['height'] == 8
    assert result['width'] == 32
    assert result['data'] == [{
        'type': 'text',
        'width': len('hello world') * 5,
        'height': 8,
        'x': 0,
        'y': 1,
        'color': 2,
        'font': 1,
        'content': 'hello world'
    }]

    app.message = ''
    app.save()
    assert app.get_app_dictionary() is None
