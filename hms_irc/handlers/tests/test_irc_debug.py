import unittest

from hms_irc.handlers import irc_debug


class TestIRCDebug(unittest.TestCase):

    def test_privmsg(self):
        body = {'privmsg': 'This is a test.'}
        self.assertEqual(body['privmsg'], irc_debug.msg_to_privmsg(body))