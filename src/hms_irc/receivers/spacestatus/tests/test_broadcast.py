from unittest.mock import Mock

import pytest

from hms_irc.receivers.spacestatus.broadcast import handle


@pytest.fixture
def irc_server():
    server = Mock()
    server.privmsg = Mock()

    return server


@pytest.fixture
def irc_chan():
    return Mock()


def test_open_twaum(irc_server, irc_chan):
    """Test that receiver prints something for twaum on opening broadcast."""
    dct = {'is_open': True}
    handle(irc_server, irc_chan, dct)
    assert(irc_server.privmsg.called)
    assert("@tweet" in irc_server.privmsg.call_args[0][1])


def test_closed_twaum(irc_server, irc_chan):
    """Test that receiver prints something for twaum on closing broadcast."""
    dct = {'is_open': False}
    handle(irc_server, irc_chan, dct)
    assert(irc_server.privmsg.called)
    assert("@tweet" in irc_server.privmsg.call_args[0][1])
