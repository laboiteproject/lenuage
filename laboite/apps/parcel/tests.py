# # coding: utf-8
# from __future__ import unicode_literals
#
# from datetime import timedelta
#
# from django.utils import timezone
# from weboob.core import Weboob
# from weboob.capabilities.base import NotLoaded
# from weboob.capabilities.parcel import CapParcel
#
# from .models import AppParcel
#
#
# PAST = timezone.now() - timedelta(seconds=AppParcel.UPDATE_INTERVAL + 1)
#
#
# def test_get_app_dictionary(monkeypatch):
#     monkeypatch.setattr(AppParcel, 'save', lambda self: True)
#     weboob = Weboob()
#     backend = weboob.load_backend('colissimo', None)
#     monkeypatch.setattr(backend.__class__, 'get_parcel_tracking', lambda parcel: {'id': 'package',
#                                                                                   'url': NotLoaded,
#                                                                                   'arrival': NotLoaded,
#                                                                                   'status': 3,
#                                                                                   'info': 'Votre colis est livré.',
#                                                                                   'history': ()})
#     app = AppParcel(created_date=PAST,
#                     last_activity=PAST,
#                     parcel='package',
#                     parcel_carrier='dhl')
#     assert app.get_app_dictionary() == {
#         'arrival': None,
#         'info': 'Votre colis est livré.',
#         'parcel': 'package',
#         'parcel_carrier': 'chronopost',
#         'status': 3,
#         'url': None,
#     }
