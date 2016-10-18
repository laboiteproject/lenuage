import operator

from .star import StarProvider


PROVIDERS = {
    'star': StarProvider
}


def get_provider(key):
    return PROVIDERS.get(key)


def get_providers():
    ret = [(key, cls.nice_name) for key, cls in PROVIDERS.iteritems()]
    ret.sort(key=operator.itemgetter(1))
    return ret


