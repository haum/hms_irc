import unittest
from unittest.mock import Mock

from hms_irc.handlers import irc_debug


class TestIRCDebug(unittest.TestCase):

    def setUp(self):
        self.body = {'privmsg': 'This is a test.'}
        self.irc_server = Mock()
        self.irc_server.privmsg = Mock()
        self.irc_chan = '#haum-test'

    def test_decode_privmsg(self):
        self.assertEqual(
            self.body['privmsg'],
            irc_debug.msg_to_privmsg(self.body))

    def test_decode_empty_privmsg(self):
        self.assertIsNone(irc_debug.msg_to_privmsg({}))

    def test_call_privmsg(self):
        irc_debug.handle(self.irc_server, self.irc_chan, self.body)

        self.irc_server.privmsg.assert_called_once_with(
            self.irc_chan, self.body['privmsg'])

    def test_call_empty_privmsg(self):
        irc_debug.handle(self.irc_server, self.irc_chan, {})

        self.irc_server.privmsg.assert_not_called()
