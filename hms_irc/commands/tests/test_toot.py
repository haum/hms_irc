import unittest

from hms_irc.commands.toot import handle
from hms_irc.commands.tests import CommandBuilder
from hms_irc.mocks import irc_server_mock, rabbit_mock


class TestToot(unittest.TestCase):

    def setUp(self):
        self.irc_server = irc_server_mock()
        self.rabbit = rabbit_mock()
        self.irc_chan = "#testhaum"
        self.cb = CommandBuilder()

        self.wrapped_handle = lambda msg: handle(self.irc_server,
                                                 self.irc_chan,
                                                 self.rabbit, msg)

    def test_toot_unvoiced(self):
        self.wrapped_handle(self.cb.args("ceci est un test").build())
        self.rabbit.publish.assert_not_called()

    def test_toot_voiced(self):
        msg = "ceci est un test"
        self.wrapped_handle(self.cb.args(msg).voiced().build())
        self.rabbit.publish.assert_called_once_with('mastodon.toot', {
            'message': msg, 'source': 'irc'})

    def test_toot_no_message(self):
        self.wrapped_handle(self.cb.build())
        self.rabbit.publish.assert_not_called()
