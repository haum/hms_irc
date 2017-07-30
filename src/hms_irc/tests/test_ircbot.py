import unittest
from unittest.mock import Mock
import signal

from irc.client import ServerConnectionError

from hms_irc.ircbot import MyBot


class ConnectionResetRequestTests(unittest.TestCase):

    """Test case that handle the connection request mechanism."""

    def setUp(self):
        self.bot = MyBot("#testhaum", "hms_irc", "freenode.net")
        self.serv = Mock()
        self.ev = Mock()

    def test_no_serv(self):
        """Test that the connection reset does not fail if no server is set."""
        self.bot.serv = None
        self.bot.handle_reconnection_request(signal.SIGUSR1, None)

    def test_with_serv(self):
        """Test that the connection reset calls connect() on the server."""
        self.bot.serv = Mock()
        self.bot.serv.connect = Mock()
        self.bot.handle_reconnection_request(signal.SIGUSR1, None)
        self.bot.serv.reconnect.assert_called_once_with()

    def test_with_serv_exception(self):
        """Test that the connection reset can handle a server error."""
        self.bot.serv = Mock()
        self.bot.serv.connect = Mock(side_effect=ServerConnectionError("test"))
        self.bot.handle_reconnection_request(signal.SIGUSR1, None)
        self.bot.serv.reconnect.assert_called_once_with()

    def test_autojoin_chan(self):
        self.serv.join = Mock()

        self.bot.on_welcome(self.serv, self.ev)

        # Verify that the bot autojoined the chan
        self.serv.join.assert_called_once_with("#testhaum")

        # Verify that the bot remembers the server for future use
        self.assertEqual(self.bot.serv, self.serv)

    def test_joined_callback(self):
        callback = Mock()
        self.bot.join_callback = callback

        self.bot.on_join(self.serv, self.ev)
        callback.assert_called_once_with()

    def test_nick_used(self):
        self.serv.get_nickname = Mock(return_value="bcazeneuve")
        self.serv.nick = Mock()

        self.bot.on_nicknameinuse(self.serv, self.ev)
        self.serv.nick.assert_called_once_with("bcazeneuve_")

    def test_privmsg(self):
        self.ev.source = "pinky!username@example.com"
        self.serv.privmsg = Mock()

        self.bot.on_privmsg(self.serv, self.ev)
        self.serv.privmsg.assert_called_once_with("pinky", "hey")
