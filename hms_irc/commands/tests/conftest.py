import pytest

from hms_irc.mocks import irc_server_mock, rabbit_mock


@pytest.fixture
def irc_server():
    return irc_server_mock()


@pytest.fixture
def rabbit():
    return rabbit_mock()


@pytest.fixture
def irc_chan():
    return "#testhaum"
