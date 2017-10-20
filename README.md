# WeekParser

This project parses an input CSV file in a specific format and produces
a formatted output of the data found in the CSV file.

## Input format

The input CSV files contain data for 5 days of a week: mon, tue, wed, thu,
fri. Days may be provided in a range format: `mon-thu`.

The input files may contain some additional data, which will be skipped.

Some example files can be found in `./csv_files/`.

Input files must be formatted as CSV and follow some rules.

For example:

```csv
mon,tue,some_column1,wed,thu,fri,description
1,5,data,2,3,3,first_desc
```

## Output format

The output will look like the following example:

```python
[{'day': 'mon', 'description': 'first_desc 1', 'square': 1, 'value': 1},
 {'day': 'tue', 'description': 'first_desc 25', 'square': 25, 'value': 5},
 {'day': 'wed', 'description': 'first_desc 4', 'square': 4, 'value': 2},
 {'day': 'thu', 'description': 'first_desc 6', 'double': 6, 'value': 3},
 {'day': 'fri', 'description': 'first_desc 6', 'double': 6, 'value': 3}]
```

For each day we store a value, description and some day's specific data:

- For mon, tue and wed it is a `square` field.
- For thu, fri it is a `double` field.

Note that the `description` field contains day's specific data.
