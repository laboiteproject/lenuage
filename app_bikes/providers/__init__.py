import operator

from .star import StarProvider
from .velib import VelibProvider


PROVIDERS = {
    'star': StarProvider,
    'velib': VelibProvider
}


def get_provider(key):
    return PROVIDERS.get(key)


def get_providers():
    ret = [(key, cls.verbose_name) for key, cls in PROVIDERS.iteritems()]
    ret.sort(key=operator.itemgetter(1))
    return ret


