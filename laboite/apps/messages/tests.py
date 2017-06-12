from .models import AppMessages


def test_message(monkeypatch):
    monkeypatch.setattr(AppMessages, 'save', lambda self: True)
    app = AppMessages(message='hello world')
    assert app.get_app_dictionary() == {'message': 'hello world'}
    app.message = ''
    assert app.get_app_dictionary() is None
