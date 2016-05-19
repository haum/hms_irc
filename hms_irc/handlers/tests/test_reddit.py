import unittest
from unittest.mock import Mock

from hms_irc.handlers import reddit


class TestRedditHandler(unittest.TestCase):

    """Test case for Reddit IRC handler."""

    def setUp(self):
        self.body = {
            'author': 'MicroJoe',
            'title': 'This is a test',
            'url': 'http://haum.org',
            'id': 'abcdef'
        }

    def test_privmsg_contains_data(self):
        privmsg = reddit.msg_to_privmsg(self.body)

        self.assertTrue(self.body['author'] in privmsg)
        self.assertTrue(self.body['title'] in privmsg)
        self.assertTrue(self.body['url'] in privmsg)

    def test_call_privmsg(self):
        irc_chan = '#haum-test'

        irc_server = Mock()
        irc_server.privmsg = Mock()

        reddit.handle(irc_server, irc_chan, self.body)

        irc_server.privmsg.assert_called_once_with(
            irc_chan,
            reddit.msg_to_privmsg(self.body))
