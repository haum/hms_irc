import unittest
from unittest.mock import Mock

from hms_irc.irc import IRCCommand
from hms_irc.transmitters.toot import handle


def mkcommand(command_args, is_voiced):
    """Builds an IRCCommand for testing purposes."""
    command = IRCCommand(
        nick = "toto",
        is_voiced = is_voiced,
        command_name = "toot",
        command_args = command_args.split(' '))

    return command


class TestToot(unittest.TestCase):

    def setUp(self):
        self.irc_server = Mock()
        self.irc_server.privmsg = Mock()

        self.irc_chan = "#testhaum"
        self.rabbit = Mock()
        self.rabbit.publish = Mock()

        self.wrapped_handle = lambda msg: handle(self.irc_server, self.irc_chan, self.rabbit, msg)

    def test_toot_unvoiced(self):
        msg = 'ceci est un test'
        self.wrapped_handle(mkcommand(msg, False))
        self.rabbit.publish.assert_not_called()

    def test_toot_voiced(self):
        msg = 'ceci est un test'
        self.wrapped_handle(mkcommand(msg, True))
        self.rabbit.publish.assert_called_once_with(
            'mastodon.toot',
            {'message': msg, 'source': 'irc'})

    def test_toot_no_message(self):
        self.wrapped_handle(mkcommand('', True))
        self.rabbit.publish.assert_not_called()