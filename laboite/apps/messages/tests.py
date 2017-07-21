from .models import AppMessages


def test_message(boite):
    app = AppMessages.objects.create(boite=boite, message='hello world')
    assert app.get_app_dictionary() == {'message': 'hello world'}

    app.message = ''
    app.save()
    assert app.get_app_dictionary() is None
