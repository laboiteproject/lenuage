class BaseProvider(object):
    verbose_name = 'BaseProvider'

    @classmethod
    def get_stations(cls):
        raise NotImplementedError()

    @classmethod
    def get_station_infos(cls, station_name_or_id):
        raise NotImplementedError()
