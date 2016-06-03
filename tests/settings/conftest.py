import pytest

import coalib.collecting.Collectors


@pytest.fixture
def disable_bears(mocker):
    """
    Disable all bears that would otherwise be found with `collect_bears(...)`.
    """
    mocker.patch.object(coalib.collecting.Collectors, '_import_bears',
                        autospec=True, return_value=[])
