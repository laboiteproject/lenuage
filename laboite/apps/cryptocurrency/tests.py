from datetime import timedelta
import decimal

from django.utils import timezone
import pytest

from .models import AppCryptocurrency

PAYLOAD = '''{
    "data": [
        {
            "id": 1, 
            "name": "Bitcoin", 
            "symbol": "BTC", 
            "website_slug": "bitcoin", 
            "rank": 1, 
            "circulating_supply": 17101312.0, 
            "total_supply": 17101312.0, 
            "max_supply": 21000000.0, 
            "quotes": {
                "USD": {
                    "price": 6741.72, 
                    "volume_24h": 4027740000.0, 
                    "market_cap": 115292257137.0, 
                    "percent_change_1h": -0.12, 
                    "percent_change_24h": 2.94, 
                    "percent_change_7d": -0.84
                }, 
                "EUR": {
                    "price": 5809.3235674278, 
                    "volume_24h": 3470693666.5230503, 
                    "market_cap": 99347054836.0, 
                    "percent_change_1h": -0.12, 
                    "percent_change_24h": 2.94, 
                    "percent_change_7d": -0.84
                }
            }, 
            "last_updated": 1529352875
        }, 
        {
            "id": 1027, 
            "name": "Ethereum", 
            "symbol": "ETH", 
            "website_slug": "ethereum", 
            "rank": 2, 
            "circulating_supply": 100157190.0, 
            "total_supply": 100157190.0, 
            "max_supply": null, 
            "quotes": {
                "USD": {
                    "price": 517.807, 
                    "volume_24h": 1517790000.0, 
                    "market_cap": 51862093855.0, 
                    "percent_change_1h": -0.31, 
                    "percent_change_24h": 2.96, 
                    "percent_change_7d": -1.23
                }, 
                "EUR": {
                    "price": 446.1930202499, 
                    "volume_24h": 1307875915.5536406, 
                    "market_cap": 44689438910.0, 
                    "percent_change_1h": -0.31, 
                    "percent_change_24h": 2.96, 
                    "percent_change_7d": -1.23
                }
            }, 
            "last_updated": 1529352861
        }, 
        {
            "id": 52, 
            "name": "Ripple", 
            "symbol": "XRP", 
            "website_slug": "ripple", 
            "rank": 3, 
            "circulating_supply": 39245304677.0, 
            "total_supply": 99991944394.0, 
            "max_supply": 100000000000.0, 
            "quotes": {
                "USD": {
                    "price": 0.537735, 
                    "volume_24h": 269810000.0, 
                    "market_cap": 21103573910.0, 
                    "percent_change_1h": -1.04, 
                    "percent_change_24h": 1.3, 
                    "percent_change_7d": -8.05
                }, 
                "EUR": {
                    "price": 0.4633649289, 
                    "volume_24h": 232494614.39034897, 
                    "market_cap": 18184897812.0, 
                    "percent_change_1h": -1.04, 
                    "percent_change_24h": 1.3, 
                    "percent_change_7d": -8.05
                }
            }, 
            "last_updated": 1529353142
        }
    ], 
    "metadata": {
        "timestamp": 1529352860, 
        "num_cryptocurrencies": 1629, 
        "error": null
    }
}'''


@pytest.fixture
def app(boite):
    d = timezone.now() - timedelta(days=1)
    return AppCryptocurrency.objects.create(created_date=d, last_activity=d,
                                            boite=boite, enabled=True)


# TODO: Update test
@pytest.mark.skip(reason="outdated test")
def test_crypto_found_usd(app, requests_mocker, settings):
    """Get Bitcoin price in dollars"""
    app.cryptocurrency = 'bitcoin'
    app.currency = 'USD'
    app.save()

    with requests_mocker as m:
        m.get(settings.COINMARKETCAP_BASE_URL, text=PAYLOAD)
        result = app.get_app_dictionary()
        assert result == {
            'width': 32,
            'height': 8,
            'data': [
                {
                    'type': 'text',
                    'width': 20,
                    'height': 8,
                    'x': 0,
                    'y': 1,
                    'color': 2,
                    'font': 1,
                    'content': '6741'
                },
                {
                    'type': 'bitmap',
                    'width': 8,
                    'height': 8,
                    'x': 20,
                    'y': 0,
                    'color': 2,
                    'content': '0x0040e08060e040'
                },
            ]
        }


# TODO: Update test
@pytest.mark.skip(reason="outdated test")
def test_crypto_found_eur(app, requests_mocker, settings):
    """Get Ethereum price in euros"""
    app.cryptocurrency = 'ethereum'
    app.currency = 'EUR'
    app.save()

    with requests_mocker as m:
        m.get(settings.COINMARKETCAP_BASE_URL, text=PAYLOAD)

        result = app.get_app_dictionary()
        assert result == {
            'width': 32,
            'height': 8,
            'data': [
                {
                    'type': 'text',
                    'width': 25,
                    'height': 8,
                    'x': 0,
                    'y': 1,
                    'color': 2,
                    'font': 1,
                    'content': '446.1'
                },
                {
                    'type': 'bitmap',
                    'width': 8,
                    'height': 8,
                    'x': 25,
                    'y': 0,
                    'color': 2,
                    'content': '0x003040e0e04030'
                },
            ]
        }


# TODO: Update test
@pytest.mark.skip(reason="outdated test")
def test_crypto_not_found(app, requests_mocker, settings):
    app.cryptocurrency = 'bloubcoin'
    app.currency = 'USD'
    app.save()

    with requests_mocker as m:
        m.get(settings.COINMARKETCAP_BASE_URL, text=PAYLOAD)

        result = app.get_app_dictionary()
        assert result == {
            'width': 32,
            'height': 8,
            'data': [
                {
                    'type': 'text',
                    'width': 5,
                    'height': 8,
                    'x': 0,
                    'y': 1,
                    'color': 2,
                    'font': 1,
                    'content': '0'
                },
                {
                    'type': 'bitmap',
                    'width': 8,
                    'height': 8,
                    'x': 5,
                    'y': 0,
                    'color': 2,
                    'content': '0x0040e08060e040'
                },
            ]
        }


# TODO: Update test
@pytest.mark.skip(reason="outdated test")
def test_format_price(app):
    app.last_activity = timezone.now()
    app.value = decimal.Decimal('0')
    app.save()
    assert app.get_app_dictionary()['data'][0]['content'] == '0'

    app.value = decimal.Decimal('0.123456')
    app.save()
    assert app.get_app_dictionary()['data'][0]['content'] == '0.123'

    app.value = decimal.Decimal('255.23333333')
    app.save()
    assert app.get_app_dictionary()['data'][0]['content'] == '255.2'


    app.value = decimal.Decimal('6340.23')
    app.save()
    assert app.get_app_dictionary()['data'][0]['content'] == '6340'
