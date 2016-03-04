import unittest

from hms_irc.handlers import reddit


class TestReddit(unittest.TestCase):

    """Test case for Reddit IRC handler."""

    def test_privmsg_contains_data(self):
        msg = {
            'author': 'MicroJoe',
            'title': 'This is a test',
            'url': 'http://haum.org'
        }

        privmsg = reddit.msg_to_privmsg(msg)

        self.assertTrue(msg['author'] in privmsg)
        self.assertTrue(msg['title'] in privmsg)
        self.assertTrue(msg['url'] in privmsg)
