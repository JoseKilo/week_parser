import pytest
import six
from mock import call, patch

from tests import utils
from week_parser.base import parse_row, parse_week, populate_extra_data
from week_parser.main import PrettyPrinter


def test_populate_extra_data_no_days():
    """
    If we haven't found any days data, there is not extra data to add
    """
    week_data = {}
    description = '__DESCRIPTION__'

    populate_extra_data(week_data, description)

    assert week_data == {}


def test_populate_extra_data_square_day():
    """
    If we have found a 'square' day, the description and square value is added
    """
    value = 7
    week_data = {'mon': {'value': value}}
    description = '__DESCRIPTION__'

    populate_extra_data(week_data, description)

    assert week_data == {
        'mon': {
            'value': value,
            'square': value ** 2,
            'description': '{} {}'.format(description, value ** 2)
        }
    }


def test_populate_extra_data_double_day():
    """
    If we have found a 'double' day, the description and double value is added
    """
    value = 7
    week_data = {'thu': {'value': value}}
    description = '__DESCRIPTION__'

    populate_extra_data(week_data, description)

    assert week_data == {
        'thu': {
            'value': value,
            'double': value * 2,
            'description': '{} {}'.format(description, value * 2)
        }
    }


def test_parse_row_single_day():
    """
    If the input row contains a single day, it is outputted
    """
    row = {'mon': '3', 'description': '__DESCRIPTION__'}

    with patch('week_parser.base.populate_extra_data') as mock_populate:
        week_data = parse_row(row)

    assert week_data == {'mon': {'day': 'mon', 'value': 3}}
    assert mock_populate.call_args_list == [call(week_data, '__DESCRIPTION__')]


def test_parse_row_day_range():
    """
    If the input row contains a day range, it is outputted
    """
    row = {'mon-wed': '3', 'description': '__DESCRIPTION__'}

    with patch('week_parser.base.populate_extra_data') as mock_populate:
        week_data = parse_row(row)

    assert week_data == {
        'mon': {'day': 'mon', 'value': 3},
        'tue': {'day': 'tue', 'value': 3},
        'wed': {'day': 'wed', 'value': 3},
    }
    assert mock_populate.call_args_list == [call(week_data, '__DESCRIPTION__')]


def test_parse_row_extra_columns():
    """
    If the input row contains any extra columns, they are skipped
    """
    row = {'wed': '2', 'description': '__DESCRIPTION__',
           '__FOO__': '__BAR__', '__ANYTHING__': '__ELSE__'}

    with patch('week_parser.base.populate_extra_data') as mock_populate:
        week_data = parse_row(row)

    assert week_data == {'wed': {'day': 'wed', 'value': 2}}
    assert mock_populate.call_args_list == [call(week_data, '__DESCRIPTION__')]


def test_parse_row_not_int_value():
    """
    If the day value is not an integer, we get a ValueError
    """
    row = {'mon': '__NOT_A_NUMBER__', 'description': '__DESCRIPTION__'}

    with patch('week_parser.base.populate_extra_data') as mock_populate:
        with pytest.raises(ValueError) as exc:
            parse_row(row)

    assert mock_populate.call_count == 0
    assert str(exc.value) == (
        "invalid literal for int() with base 10: '__NOT_A_NUMBER__'")


def test_parse_row_invalid_day_range():
    """
    If the input row contains an invalid day range, we skip it
    """
    row = {'foo-bar': '3', 'description': '__DESCRIPTION__'}

    with patch('week_parser.base.populate_extra_data') as mock_populate:
        week_data = parse_row(row)

    assert week_data == {}
    assert mock_populate.call_args_list == [call(week_data, '__DESCRIPTION__')]


def test_parse_row():
    """
    An input row may contain any combination of day ranges
    """
    row = {'mon-tue': '3', 'wed-thu': '2', 'fri': '1',
           '__SOME__': '__DATA__', 'description': '__DESCRIPTION__'}

    with patch('week_parser.base.populate_extra_data') as mock_populate:
        week_data = parse_row(row)

    assert week_data == {
        'mon': {'day': 'mon', 'value': 3},
        'tue': {'day': 'tue', 'value': 3},
        'wed': {'day': 'wed', 'value': 2},
        'thu': {'day': 'thu', 'value': 2},
        'fri': {'day': 'fri', 'value': 1},
    }
    assert mock_populate.call_args_list == [call(week_data, '__DESCRIPTION__')]


def test_parse_week_empty_file():
    """
    We can process an empty file
    """
    filename = 'anything.csv'

    with utils.mock_open(file_content='') as mock_open:
        with patch('week_parser.base.parse_row') as mock_parse_week:
            result = parse_week(filename)

    assert result == []
    assert mock_open.call_args_list == [call(filename)]
    assert mock_parse_week.call_count == 0


def test_parse_week_valid_file():
    """
    We can process a file with valid content
    """
    filename = 'anything.csv'
    csv_data = ('mon,tue,some_column1,wed,thu,fri,description\n'
                '1,5,data,2,3,3,first_desc\n')
    expected_row = {'mon': '1', 'tue': '5', 'wed': '2', 'thu': '3', 'fri': '3',
                    'description': 'first_desc', 'some_column1': 'data'}

    with utils.mock_open(file_content=csv_data) as mock_open:
        with patch('week_parser.base.parse_row') as mock_parse_row:
            mock_parse_row.return_value = {'mon': {'day': 'mon'}}

            result = parse_week(filename)

    assert result == [{'day': 'mon'}]
    assert mock_open.call_args_list == [call(filename)]
    assert mock_parse_row.call_args_list == [call(expected_row)]


def test_pprint_bytes(capsys):
    printer = PrettyPrinter()

    printer.pprint(six.b('__FOO__'))

    out, err = capsys.readouterr()
    assert err == ''
    assert out == "'__FOO__'\n"


def test_pprint_unicode(capsys):
    printer = PrettyPrinter()

    printer.pprint(six.u('__FOO__'))

    out, err = capsys.readouterr()
    assert err == ''
    assert out == "'__FOO__'\n"
