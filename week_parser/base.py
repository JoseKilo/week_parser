import csv

import six


DAYS = ('mon', 'tue', 'wed', 'thu', 'fri')
SQUARE_DAYS = ('mon', 'tue', 'wed')
DOUBLE_DAYS = ('thu', 'fri')

DAY_TO_NUMBER = {day: i for i, day in enumerate(DAYS)}
NUMBER_TO_DAY = {i: day for i, day in enumerate(DAYS)}


def parse_week(filename):
    """
    We open an input filename, parse it and return its data.
    """
    week_data = {}

    with open(filename) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            week_data = parse_row(row)

    return [week_data[day] for day in DAYS]


def parse_row(row):
    """
    Parse a row from an input CSV file and return its data.

    The expected input format is a dictionary of column_names -> column_values.
    """
    week_data = {}
    description = None

    for column, value in six.iteritems(row):
        if column == 'description':
            description = value
        elif column in DAYS:
            week_data[column] = {'day': column, 'value': int(value)}
        elif column is not None and '-' in column:
            start, end = column.split('-')
            start, end = DAY_TO_NUMBER[start], DAY_TO_NUMBER[end]

            for number in six.moves.xrange(start, end + 1):
                day = NUMBER_TO_DAY[number]
                week_data[day] = {'day': day, 'value': int(value)}

    populate_extra_data(week_data, description)

    return week_data


def populate_extra_data(week_data, description):
    """
    Once the daily data has been collected, we need to append the extra value
    and the description to every day.
    """
    for day, day_week_data in six.iteritems(week_data):
        value = day_week_data['value']
        if day in SQUARE_DAYS:
            extra_value = value ** 2
            day_week_data['square'] = extra_value
        elif day in DOUBLE_DAYS:
            extra_value = value * 2
            day_week_data['double'] = extra_value
        day_week_data['description'] = '{} {}'.format(description, extra_value)
