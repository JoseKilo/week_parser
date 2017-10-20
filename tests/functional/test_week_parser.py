import os
from argparse import Namespace

import pytest

from week_parser.main import get_options, main


expected_output_1 = (
    """[{'day': 'mon', 'description': 'first_desc 1', 'square': 1, 'value': 1},
 {'day': 'tue', 'description': 'first_desc 25', 'square': 25, 'value': 5},
 {'day': 'wed', 'description': 'first_desc 4', 'square': 4, 'value': 2},
 {'day': 'thu', 'description': 'first_desc 6', 'double': 6, 'value': 3},
 {'day': 'fri', 'description': 'first_desc 6', 'double': 6, 'value': 3}]
"""
)

expected_output_2 = (
    """[{'day': 'mon', 'description': 'second_desc 4', 'square': 4, 'value': 2},
 {'day': 'tue', 'description': 'second_desc 4', 'square': 4, 'value': 2},
 {'day': 'wed', 'description': 'second_desc 4', 'square': 4, 'value': 2},
 {'day': 'thu', 'description': 'second_desc 4', 'double': 4, 'value': 2},
 {'day': 'fri', 'description': 'second_desc 6', 'double': 6, 'value': 3}]
"""
)

expected_output_3 = (
    """[{'day': 'mon', 'description': 'third_desc 9', 'square': 9, 'value': 3},
 {'day': 'tue', 'description': 'third_desc 9', 'square': 9, 'value': 3},
 {'day': 'wed', 'description': 'third_desc 4', 'square': 4, 'value': 2},
 {'day': 'thu', 'description': 'third_desc 4', 'double': 4, 'value': 2},
 {'day': 'fri', 'description': 'third_desc 2', 'double': 2, 'value': 1}]
"""
)

missing_days_output = (
    """[{'day': 'mon', 'description': 'third_desc 9', 'square': 9, 'value': 3},
 {'day': 'tue', 'description': 'third_desc 9', 'square': 9, 'value': 3},
 {'day': 'wed', 'description': 'third_desc 4', 'square': 4, 'value': 2},
 {'day': 'fri', 'description': 'third_desc 2', 'double': 2, 'value': 1}]
"""
)


test_files = {
    os.path.join('csv_files', '1.csv'): expected_output_1,
    os.path.join('csv_files', '2.csv'): expected_output_2,
    os.path.join('csv_files', '3.csv'): expected_output_3,
    os.path.join('csv_files', 'column_no_name.csv'): expected_output_3,
    os.path.join('csv_files', 'multiple_rows.csv'): expected_output_3,
    os.path.join('csv_files', 'missing_days.csv'): missing_days_output,
    os.path.join('csv_files', 'empty.csv'): '[]\n',
    os.path.join('csv_files', 'only_headers.csv'): '[]\n',
}


def test_main(capsys):
    """
    All the example input files produce the expected output
    """
    for filename, expected_output in test_files.items():

        main([filename])

        out, err = capsys.readouterr()
        assert err == ''
        assert out == expected_output


def test_main_file_does_not_exist(capsys):
    """
    If the input file doesn't exist, we get an error message
    """
    filename = 'does_not_exist.csv'

    main([filename])

    out, err = capsys.readouterr()
    assert out == ''
    assert err == 'No such file or directory\n'


def test_main_not_int_value(capsys):
    """
    If the day value is not an integer, we get an error message
    """
    filename = os.path.join('csv_files', 'not_int_value.csv')

    main([filename])

    out, err = capsys.readouterr()
    assert out == ''
    assert err == ("Invalid file format: "
                   "invalid literal for int() with base 10: 'not an int'\n")


def test_get_options():
    """
    A valid path argument will produce a valid argparse object
    """
    filename = 'anything.csv'
    options = get_options([filename])

    assert options == Namespace(filename=filename)


def test_get_options_help(capsys):
    """
    A '--help' flag shows some usage help
    """
    with pytest.raises(SystemExit):
        get_options(['--help'])

    out, err = capsys.readouterr()
    assert err == ''
    assert out.startswith('usage:')
    assert 'WeekParser' in out


def test_get_options_invalid(capsys):
    """
    An invalid sequence of arguments will produce some usage help
    """
    with pytest.raises(SystemExit):
        get_options(['one_file.csv', 'another_file.csv'])

    out, err = capsys.readouterr()
    assert out == ''
    assert err.startswith('usage:')
    assert 'unrecognized argument' in err
