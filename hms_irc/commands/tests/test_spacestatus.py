import unittest

from hms_irc.commands.spacestatus import handle
from hms_irc.commands.tests import CommandBuilder, irc_server_mock, rabbit_mock


class SpaceStatusTest(unittest.TestCase):

    def setUp(self):
        self.irc_server = irc_server_mock()
        self.rabbit = rabbit_mock()
        self.irc_chan = "#testhaum"
        self.cb = CommandBuilder()

        self.wrapped_handle = lambda msg: handle(self.irc_server, self.irc_chan,
                                                 self.rabbit, msg)

    def test_invalid_argument(self):
        """Calls the spacestatus command with invalid argument"""
        self.wrapped_handle(self.cb.args("lolilol").build())
        self.rabbit.publish.assert_not_called()

    def test_check_status(self):
        """Check that anyone can check the space status."""
        self.wrapped_handle(self.cb.build())
        self.rabbit.publish.assert_called_with('spacestatus.query', {
            'command': 'status',
            'source': 'irc'
        })

    def test_help(self):
        """Check that the help does not publish a message."""
        self.wrapped_handle(self.cb.args("help").build())
        self.rabbit.publish.assert_not_called()

    def test_open_not_voiced(self):
        """Test to open the space with non-voiced user."""
        self.wrapped_handle(self.cb.args("open").build())
        self.rabbit.assert_not_called()

    def test_open_voiced(self):
        """Test to open the space with voiced user."""
        self.wrapped_handle(self.cb.args("open").voiced().build())
        self.rabbit.publish.assert_called_with('spacestatus.query', {
            'command': 'open',
            'source': 'irc'
        })