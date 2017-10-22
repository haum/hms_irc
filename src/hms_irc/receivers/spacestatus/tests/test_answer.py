from unittest.mock import Mock

import pytest

from hms_irc.receivers.spacestatus.answer import handle


@pytest.fixture
def irc_server():
    server = Mock()
    server.privmsg = Mock()

    return server


@pytest.fixture
def irc_chan():
    return Mock()


def test_opened(irc_server, irc_chan):
    """Test that the receiver prints on opening answer."""
    dct = {'is_open': True}
    handle(irc_server, irc_chan, dct)
    assert (irc_server.privmsg.called)


def test_opened_same_state(irc_server, irc_chan):
    """Test that the receiver prints on opening answer (same state)."""
    dct = {'is_open': True, 'has_changed': False}
    handle(irc_server, irc_chan, dct)
    assert (irc_server.privmsg.called)


def test_closed(irc_server, irc_chan):
    """Test that the receiver prints on closing answer."""
    dct = {'is_open': False}
    handle(irc_server, irc_chan, dct)
    assert (irc_server.privmsg.called)


def test_closed_same_state(irc_server, irc_chan):
    """Test that the receiver prints on closing answer (same state)."""
    dct = {'is_open': False, 'has_changed': False}
    handle(irc_server, irc_chan, dct)
    assert(irc_server.privmsg.called)
