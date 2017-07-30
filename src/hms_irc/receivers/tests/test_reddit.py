import pytest

from hms_irc.receivers import reddit
from hms_irc.mocks import irc_server_mock


@pytest.fixture
def message():
    return {
        'author': 'MicroJoe',
        'title': 'This is a test',
        'url': 'http://haum.org',
        'id': 'abcdef'
    }


@pytest.fixture
def irc_server():
    return irc_server_mock()


def test_privmsg_contains_data(message):
    privmsg = reddit.msg_to_privmsg(message)

    assert(message['author'] in privmsg)
    assert(message['title'] in privmsg)
    assert(message['url'] in privmsg)


def test_call_privmsg(irc_server, message):
    irc_chan = '#haum-test'
    reddit.handle(irc_server, irc_chan, message)

    irc_server.privmsg.assert_called_once_with(
        irc_chan,
        reddit.msg_to_privmsg(message))
