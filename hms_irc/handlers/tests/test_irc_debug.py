import unittest
from unittest.mock import Mock

from hms_irc.handlers import irc_debug


class TestIRCDebug(unittest.TestCase):

    def setUp(self):
        self.body = {'privmsg': 'This is a test.'}

    def test_decode_privmsg(self):
        self.assertEqual(
            self.body['privmsg'],
            irc_debug.msg_to_privmsg(self.body))

    def test_call_privmsg(self):
        irc_chan = '#haum-test'

        irc_server = Mock()
        irc_server.privmsg = Mock()

        irc_debug.handle(irc_server, irc_chan, self.body)

        irc_server.privmsg.assert_called_with(irc_chan, self.body['privmsg'])
