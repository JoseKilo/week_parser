from contextlib import contextmanager

from mock import mock_open as original_mock_open
from mock import patch


@contextmanager
def mock_open(file_content):
    """
    Mock '__builtin__.open' with the content provided

    Bug work-around: https://bugs.python.org/issue21258
    """
    mock = original_mock_open(read_data=file_content)
    with patch('six.moves.builtins.open', mock) as mocked_open:
        mock.return_value.__iter__ = lambda self: iter(self.readline, '')
        yield mocked_open
