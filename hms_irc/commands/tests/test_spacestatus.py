import unittest
from unittest.mock import Mock

from hms_irc.irc import IRCCommand
from hms_irc.commands.spacestatus import handle


def mkcommand(command_args, is_voiced):
    """Builds an IRCCommand for testing purposes."""
    command = IRCCommand(
        nick = "toto",
        is_voiced = is_voiced,
        command_name = "spacestatus",
        command_args = command_args.split(' '))

    if command.command_args == ['']:
        command.command_args = None

    return command


class SpaceStatusTest(unittest.TestCase):

    def setUp(self):
        self.irc_server = Mock()
        self.irc_server.privmsg = Mock()

        self.irc_chan = "#testhaum"
        self.rabbit = Mock()
        self.rabbit.publish = Mock()

        self.wrapped_handle = lambda msg: handle(self.irc_server, self.irc_chan,
                                                 self.rabbit, msg)

    def test_invalid_argument(self):
        """Calls the spacestatus command with invalid argument"""
        command = mkcommand("lolilol", False)
        self.wrapped_handle(command)
        self.rabbit.publish.assert_not_called()

    def test_check_status(self):
        """Check that anyone can check the space status."""
        command = mkcommand("", False)
        self.wrapped_handle(command)
        self.rabbit.publish.assert_called_with('spacestatus.query', {
            'command': 'status',
            'source': 'irc'
        })

    def test_help(self):
        """Check that the help does not publish a message."""
        command = mkcommand("help", False)
        self.wrapped_handle(command)
        self.rabbit.publish.assert_not_called()

    def test_open_not_voiced(self):
        """Test to open the space with non-voiced user."""
        command = mkcommand("open", False)
        self.wrapped_handle(command)
        self.rabbit.assert_not_called()

    def test_open_voiced(self):
        """Test to open the space with voiced user."""
        command = mkcommand("open", True)
        self.wrapped_handle(command)
        self.rabbit.publish.assert_called_with('spacestatus.query', {
            'command': 'open',
            'source': 'irc'
        })