import unittest
from unittest.mock import Mock
import signal

from irc.client import ServerConnectionError

from hms_irc.ircbot import MyBot


class ConnectionResetRequestTests(unittest.TestCase):

    """Test case that handle the connection request mechanism."""

    def setUp(self):
        self.bot = MyBot("#testhaum", "hms_irc", "freenode.net")

    def test_no_serv(self):
        """Test that the connection reset does not fail if no server is set."""
        self.bot.serv = None
        self.bot.handle_reconnection_request(signal.SIGUSR1, None)

    def test_with_serv(self):
        """Test that the connection reset calls connect() on the server."""
        self.bot.serv = Mock()
        self.bot.serv.connect = Mock()
        self.bot.handle_reconnection_request(signal.SIGUSR1, None)
        self.bot.serv.connect.assert_called_once()

    def test_with_serv_exception(self):
        """Test that the connection reset can handle a server error properly."""
        self.bot.serv = Mock()
        self.bot.serv.connect = Mock(side_effect=ServerConnectionError("test"))
        self.bot.handle_reconnection_request(signal.SIGUSR1, None)
        self.bot.serv.connect.assert_called_once()