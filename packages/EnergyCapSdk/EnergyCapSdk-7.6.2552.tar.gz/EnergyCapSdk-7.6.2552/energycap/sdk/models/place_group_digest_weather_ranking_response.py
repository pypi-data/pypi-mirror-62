# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PlaceGroupDigestWeatherRankingResponse(Model):
    """PlaceGroupDigestWeatherRankingResponse.

    :param high_weather_load:
    :type high_weather_load: float
    :param low_weather_load:
    :type low_weather_load: float
    :param average_weather_load:
    :type average_weather_load: float
    :param median_weather_load:
    :type median_weather_load: float
    :param high_non_weather_load:
    :type high_non_weather_load: float
    :param low_non_weather_load:
    :type low_non_weather_load: float
    :param average_non_weather_load:
    :type average_non_weather_load: float
    :param median_non_weather_load:
    :type median_non_weather_load: float
    :param results:
    :type results:
     list[~energycap.sdk.models.PlaceGroupDigestWeatherRankingChild]
    :param place_group_id:
    :type place_group_id: int
    :param place_group_code:
    :type place_group_code: str
    :param place_group_info:
    :type place_group_info: str
    :param place_group_display: This is the user's preferred way of viewing
     this entity - could be code or info based on the master "data object view"
     setting in DB
    :type place_group_display: str
    :param benchmark_unit: This will provide the benchmark unit eg:MMBTU/ft²
     or $/day
    :type benchmark_unit: str
    :param benchmark_factor_unit: This will provide the unit for the
     benchmarking factor eg:ft² or day
    :type benchmark_factor_unit: str
    :param benchmark_value_unit: This will provide the unit for the benchmark
     value eg:$ for cost/day, MMBTU for annualized use/area
    :type benchmark_value_unit: str
    :param use_unit: The use unit of measure
    :type use_unit: ~energycap.sdk.models.UnitChild
    :param cost_unit: The cost unit of measure
    :type cost_unit: ~energycap.sdk.models.UnitChild
    :param updated: The date and time the data was updated
    :type updated: datetime
    """

    _attribute_map = {
        'high_weather_load': {'key': 'highWeatherLoad', 'type': 'float'},
        'low_weather_load': {'key': 'lowWeatherLoad', 'type': 'float'},
        'average_weather_load': {'key': 'averageWeatherLoad', 'type': 'float'},
        'median_weather_load': {'key': 'medianWeatherLoad', 'type': 'float'},
        'high_non_weather_load': {'key': 'highNonWeatherLoad', 'type': 'float'},
        'low_non_weather_load': {'key': 'lowNonWeatherLoad', 'type': 'float'},
        'average_non_weather_load': {'key': 'averageNonWeatherLoad', 'type': 'float'},
        'median_non_weather_load': {'key': 'medianNonWeatherLoad', 'type': 'float'},
        'results': {'key': 'results', 'type': '[PlaceGroupDigestWeatherRankingChild]'},
        'place_group_id': {'key': 'placeGroupId', 'type': 'int'},
        'place_group_code': {'key': 'placeGroupCode', 'type': 'str'},
        'place_group_info': {'key': 'placeGroupInfo', 'type': 'str'},
        'place_group_display': {'key': 'placeGroupDisplay', 'type': 'str'},
        'benchmark_unit': {'key': 'benchmarkUnit', 'type': 'str'},
        'benchmark_factor_unit': {'key': 'benchmarkFactorUnit', 'type': 'str'},
        'benchmark_value_unit': {'key': 'benchmarkValueUnit', 'type': 'str'},
        'use_unit': {'key': 'useUnit', 'type': 'UnitChild'},
        'cost_unit': {'key': 'costUnit', 'type': 'UnitChild'},
        'updated': {'key': 'updated', 'type': 'iso-8601'},
    }

    def __init__(self, high_weather_load=None, low_weather_load=None, average_weather_load=None, median_weather_load=None, high_non_weather_load=None, low_non_weather_load=None, average_non_weather_load=None, median_non_weather_load=None, results=None, place_group_id=None, place_group_code=None, place_group_info=None, place_group_display=None, benchmark_unit=None, benchmark_factor_unit=None, benchmark_value_unit=None, use_unit=None, cost_unit=None, updated=None):
        super(PlaceGroupDigestWeatherRankingResponse, self).__init__()
        self.high_weather_load = high_weather_load
        self.low_weather_load = low_weather_load
        self.average_weather_load = average_weather_load
        self.median_weather_load = median_weather_load
        self.high_non_weather_load = high_non_weather_load
        self.low_non_weather_load = low_non_weather_load
        self.average_non_weather_load = average_non_weather_load
        self.median_non_weather_load = median_non_weather_load
        self.results = results
        self.place_group_id = place_group_id
        self.place_group_code = place_group_code
        self.place_group_info = place_group_info
        self.place_group_display = place_group_display
        self.benchmark_unit = benchmark_unit
        self.benchmark_factor_unit = benchmark_factor_unit
        self.benchmark_value_unit = benchmark_value_unit
        self.use_unit = use_unit
        self.cost_unit = cost_unit
        self.updated = updated
