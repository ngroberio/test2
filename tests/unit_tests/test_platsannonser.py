from sokannonser.repository import elastic, platsannonser
from sokannonser.repository.querybuilder import QueryBuilder
from sokannonser import settings
from valuestore import taxonomy as t
from valuestore.taxonomy import tax_type
from dateutil import parser
import sys, pytest, logging

log = logging.getLogger(__name__)
pbquery = QueryBuilder()


@pytest.mark.unit
@pytest.mark.parametrize("from_datetime", ["2018-09-28T00:00:00", '2018-09-28', '', None, []])
@pytest.mark.parametrize("to_datetime", ["2018-09-28T00:01", '2018-09-27', '', None, []])
def test_filter_timeframe(from_datetime, to_datetime):
    print('============================', sys._getframe().f_code.co_name, '============================ ')
    print(from_datetime, to_datetime)
    if not from_datetime and not to_datetime:  # from and to date are empty
        assert pbquery._filter_timeframe(from_datetime, to_datetime) is None
        return
    if from_datetime and to_datetime:
        d = pbquery._filter_timeframe(parser.parse(from_datetime), parser.parse(to_datetime))
        print(d)
        assert d['range']['publiceringsdatum']['gte'] == parser.parse(from_datetime).isoformat()
        assert d['range']['publiceringsdatum']['lte'] == parser.parse(to_datetime).isoformat()
        return
    if from_datetime:
        d = pbquery._filter_timeframe(parser.parse(from_datetime), to_datetime)
        assert d['range']['publiceringsdatum']['gte'] == parser.parse(from_datetime).isoformat()
        return
    if to_datetime:
        d = pbquery._filter_timeframe(from_datetime, parser.parse(to_datetime))
        assert d['range']['publiceringsdatum']['lte'] == parser.parse(to_datetime).isoformat()

        
@pytest.mark.unit
@pytest.mark.parametrize("args, exist, expected", [({settings.APIKEY: "",
                                                     settings.LONGITUDE: 17.1,
                                                     settings.LATITUDE: 60.5,
                                                     settings.POSITION_RADIUS: 5},
                                                    True,
                                                    {"geo_distance": {"distance": "5km",
                                                                      "arbetsplatsadress.coordinates": [
                                                                          17.1, 60.5
                                                                      ]}}),
                                                   ({settings.APIKEY: "",
                                                     settings.LONGITUDE: 399.1,
                                                     settings.LATITUDE: 60.5,
                                                     settings.POSITION_RADIUS: 5},
                                                    False,
                                                    {"geo_distance": {"distance": "5km",
                                                                      "arbetsplatsadress.coordinates": [
                                                                          399.1, 60.5
                                                                      ]}}),
                                                   ({settings.APIKEY: "",
                                                     settings.LONGITUDE: 17.1,
                                                     settings.LATITUDE: 60.5,
                                                     settings.POSITION_RADIUS: -5},
                                                    False,
                                                    {"geo_distance": {"distance": "-5km",
                                                                      "arbetsplatsadress.coordinates": [
                                                                          17.1, 60.5
                                                                      ]}})])
def test_geo_distance_filter(args, exist, expected):
    print('============================', sys._getframe().f_code.co_name, '============================ ')
    query_dsl = pbquery.parse_args(args)
    assert (expected in query_dsl["query"]["bool"]["filter"]) == exist
    
