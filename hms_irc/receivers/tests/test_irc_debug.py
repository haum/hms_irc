import pytest

from hms_irc.receivers import irc_debug
from hms_irc.mocks import irc_server_mock


@pytest.fixture
def message():
    return {'privmsg': 'This is a test.'}


@pytest.fixture
def irc_chan():
    return '#haum-test'


@pytest.fixture
def irc_server():
    return irc_server_mock()


def test_decode_privmsg(message):
    assert(message['privmsg'] == irc_debug.msg_to_privmsg(message))


def test_decode_empty_privmsg():
    assert(irc_debug.msg_to_privmsg({}) is None)


def test_call_privmsg(message, irc_chan, irc_server):
    irc_debug.handle(irc_server, irc_chan, message)
    irc_server.privmsg.assert_called_once_with(
        irc_chan, message['privmsg'])


def test_call_empty_privmsg(irc_server, irc_chan):
    irc_debug.handle(irc_server, irc_chan, {})
    irc_server.privmsg.assert_not_called()
