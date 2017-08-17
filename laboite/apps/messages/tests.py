from .models import AppMessages


def test_message(boite):
    app = AppMessages.objects.create(boite=boite, message='hello world')
    assert app.get_app_dictionary() == {
                                        'width': 32,
                                        'height': 8,
                                        'update-interval': None,
                                        'text-message': {
                                            'type': 'text',
                                            'width': len('hello world') * 5,
                                            'height': 8,
                                            'x': 0,
                                            'y': 1,
                                            'scrolling':True,
                                            'content': 'hello world',}}

    app.message = ''
    app.save()
    assert app.get_app_dictionary() is None
